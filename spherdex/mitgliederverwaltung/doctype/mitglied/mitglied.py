# Copyright (c) 2025, Thomas Dannenberg and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate
from frappe.model.naming import getseries
from ....global_scripts import initialen, serial
import json, os, datetime, tempfile, time, csv
from frappe.utils.file_manager import save_file
from frappe import _

class Mitglied(Document):
    def autoname(self):
        """Generiert die Mitgliedsnummer basierend auf den Einstellungen"""
        SETTINGS = frappe.get_single("Mitgliederverwaltung Einstellungen")

        # Präfix und Format aus den Einstellungen
        PREFIX = SETTINGS.nummer_praefix or "UNB"
        FORMAT_STRING = SETTINGS.nummer_format or "<YY><Initialen><MM><####>"
        STARTNUMMER = SETTINGS.start_nummer or 1

        # Eintrittsdatum prüfen und konvertieren
        if not self.eintrittsdatum:
            frappe.throw("Eintrittsdatum muss angegeben werden.")
        EINTRITTSDATUM = getdate(self.eintrittsdatum)
        YEAR = EINTRITTSDATUM.strftime("%y")  # Zwei Ziffern des Jahres
        FULL_YEAR = EINTRITTSDATUM.strftime("%Y")  # Volles Jahr
        MONTH = EINTRITTSDATUM.strftime("%m")  # Monat
        DAY = EINTRITTSDATUM.strftime("%d")  # Tag

        # Initialen generieren
        INITIALEN = initialen.get_initialen(self.vorname, self.nachname)

        # Laufende Nummer basierend auf Präfix
        SERIES_LENGTH = serial.get_serie_length(FORMAT_STRING)

        # Seriennummer generieren basierend auf Präfix
        SERIENNUMMER = serial.get_serial(PREFIX, STARTNUMMER, SERIES_LENGTH)

        # Seriennummer ins Hidden Field schreiben
        self.seriennummer = int(SERIENNUMMER)

        # Formatlänge anpassen
        LENGTH = ""
        count = 0
        while count < SERIES_LENGTH:
            LENGTH += "#"
            count += 1

        # Nummer zusammensetzen
        self.name = f"{PREFIX}-"+(
            FORMAT_STRING
            .replace("<YY>", YEAR)
            .replace("<YYYY>", FULL_YEAR)
            .replace("<MM>", MONTH)
            .replace("<DD>", DAY)
            .replace("<Initialen>", INITIALEN)
            .replace(f"<{LENGTH}>", SERIENNUMMER)
        )

@frappe.whitelist()
def export_members_csv_async(fields="[]", only_active="false"):
    """Startet den CSV-Export als Hintergrund-Job."""
    try:
        frappe.logger().info("📤 Versuche, Export-Job zu enqueuen...")
        job = frappe.enqueue(
            "spherdex.mitgliederverwaltung.doctype.mitglied.mitglied.export_members_csv",
            queue="long",
            timeout=300,
            job_name="Mitglieder-CSV-Export",
            is_async=True,
            fields=fields,
            only_active=only_active
        )
        frappe.logger().info(f"✅ Job erfolgreich gestartet: {job.get_id()}")
        return {"status": "Export gestartet", "job_id": job.get_id() if job else "Fehlgeschlagen"}
    except Exception as e:
        frappe.logger().error(f"❌ Fehler beim Enqueuen: {str(e)}")
        return {"status": "Fehler", "message": str(e)}

@frappe.whitelist()
def export_members_csv(fields="[]", only_active="false"):
    """CSV-Export mit echten Mitgliedsdaten."""
    fields = json.loads(fields)
    only_active = only_active.lower() == "true"

    frappe.cache().set_value("export_ready", False)

    filename = "Mitgliederliste_export.csv"
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)

    try:
        frappe.logger().info(f"📂 Speichere Datei in temporärem Ordner: {file_path}")

        # ✅ Datenbankabfrage: Mitglieder mit den ausgewählten Feldern abrufen
        filters = {"status": "Aktiv"} if only_active else {}
        mitglieder = frappe.get_all("Mitglied", filters=filters, fields=fields)

        # ✅ Datei schreiben
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # ✅ Spaltenüberschriften aus den Feldern schreiben
            writer.writerow(fields)

            # ✅ Mitgliedsdaten einfügen
            for mitglied in mitglieder:
                writer.writerow([mitglied[field] for field in fields])

        # ✅ Dateiinhalt als Bytes laden
        with open(file_path, mode="rb") as file:
            file_content = file.read()

        # ✅ Datei in ERPNext speichern
        file_doc = save_file(filename, file_content, "Mitglied", "Mitgliederliste-Export", is_private=1)

        # ✅ Temporäre Datei löschen
        os.remove(file_path)

        frappe.logger().info(f"✅ Export abgeschlossen: {file_doc.file_url}")
        frappe.publish_realtime("export_complete", {"status": "success", "file_url": file_doc.file_url})

        frappe.cache().set_value("export_ready", True)

        return file_doc.file_url

    except Exception as e:
        frappe.logger().error(f"❌ Fehler beim Schreiben der Datei: {str(e)}")
        frappe.throw(_("Fehler beim Export: {0}").format(str(e)))


@frappe.whitelist()
def is_export_ready():
    """Gibt zurück, ob der Export bereit ist (aus Cache)"""
    ready = frappe.cache().get_value("export_ready") or False
    return {"export_ready": ready}
    
@frappe.whitelist()
def delete_export_files():
    """Löscht alle CSV-Exportdateien vom Server und entfernt die Datenbankeinträge."""
    
    base_filename = "Mitgliederliste_export"
    site_path = frappe.get_site_path("private/files/")
    
    try:
        # 🔍 **Alle passenden Dateien finden (unabhängig von der Endung)**
        matching_files = [f for f in os.listdir(site_path) if f.startswith(base_filename)]

        # 🔥 **Dateien vom Server löschen**
        for file in matching_files:
            file_path = os.path.join(site_path, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                frappe.logger().info(f"🗑 Gelöscht: {file_path}")

        # 🔥 **Datenbank-Einträge in `tabFile` löschen**
        frappe.db.delete("File", {"file_name": ("like", base_filename + "%")})
        frappe.db.commit()

        return {"status": "success", "message": f"{len(matching_files)} Datei(en) gelöscht."}

    except Exception as e:
        frappe.logger().error(f"❌ Fehler beim Löschen: {str(e)}")
        return {"status": "error", "message": str(e)}