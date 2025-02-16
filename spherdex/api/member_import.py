import frappe
import csv
import os
from datetime import datetime, date

@frappe.whitelist()
def upload_csv(file_url):
    if not file_url:
        frappe.throw("❌ Keine Datei-URL empfangen!")

    # **Dateipfad berechnen**
    file_path = frappe.get_site_path(file_url.lstrip("/")) if file_url.startswith("/private/files/") else frappe.get_site_path("private" + file_url)

    if not os.path.exists(file_path):
        frappe.throw(f"❌ Datei nicht gefunden: {file_path}")

    created_members = 0
    updated_members = 0
    ignored_members = 0

    # **Datenbankfelder dynamisch abrufen**
    member_meta = frappe.get_meta("Mitglied")
    db_fields = {df.fieldname for df in member_meta.fields}

    # **Hilfsfunktion: Datum für Speicherung in DB (`DD.MM.YYYY` ➝ `YYYY-MM-DD`)**
    def to_db_date(value):
        try:
            return datetime.strptime(value.strip(), "%d.%m.%Y").strftime("%Y-%m-%d")
        except (ValueError, AttributeError):
            return value  

    # **CSV-Datei einlesen**
    with open(file_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        csv_fields = set(reader.fieldnames)

        # **Prüfen, ob alle Datenbankfelder in der CSV enthalten sind**
        missing_fields = db_fields - csv_fields
        if missing_fields:
            frappe.throw(f"❌ Fehlende Felder in CSV: {', '.join(missing_fields)}")

        for row in reader:
            vorname = row.get("vorname", "").strip() if row.get("vorname") else ""
            nachname = row.get("nachname", "").strip() if row.get("nachname") else ""
            eintrittsdatum = to_db_date(row.get("eintrittsdatum", ""))

            # **Mitglied in DB suchen**
            existing_member = frappe.db.get_value(
                "Mitglied",
                {"vorname": vorname, "nachname": nachname, "eintrittsdatum": eintrittsdatum},
                "name"
            )

            if existing_member:
                member_doc = frappe.get_doc("Mitglied", existing_member)
                changes_made = False

                for field in db_fields:
                    cleaned_value = row.get(field, "") if row.get(field) else ""

                    if isinstance(cleaned_value, str):
                        cleaned_value = cleaned_value.strip()

                    # **Falls Feld ein Datum ist, für DB speichern**
                    if field in ["geburtstag", "eintrittsdatum", "austritsdatum"]:
                        cleaned_value = to_db_date(cleaned_value)

                    # **Wert aus der DB abrufen und sicherstellen, dass er `str` ist**
                    existing_value = member_doc.get(field)

                    if isinstance(existing_value, date):
                        existing_value = existing_value.strftime("%Y-%m-%d")  

                    if cleaned_value and existing_value != cleaned_value:
                        member_doc.set(field, cleaned_value)
                        changes_made = True

                if changes_made:
                    try:
                        member_doc.save()
                        frappe.db.commit()
                        updated_members += 1
                    except Exception:
                        ignored_members += 1
                else:
                    ignored_members += 1
            else:
                # **Neues Mitglied anlegen**
                try:
                    new_member = frappe.new_doc("Mitglied")

                    for field in db_fields:
                        cleaned_value = row.get(field, "") if row.get(field) else ""

                        if isinstance(cleaned_value, str):
                            cleaned_value = cleaned_value.strip()

                        if field in ["geburtstag", "eintrittsdatum", "austritsdatum"]:
                            cleaned_value = to_db_date(cleaned_value)

                        new_member.set(field, cleaned_value)

                    new_member.insert()
                    frappe.db.commit()
                    created_members += 1
                except Exception:
                    ignored_members += 1

    # **Nach dem Import: Datei vom Server und aus der DB löschen**
    deleted_file_name = file_url.split("/")[-1]  # **Nur den Dateinamen extrahieren**
    try:
        if os.path.exists(file_path):
            os.remove(file_path)

        # **Datei aus der Frappe-Datenbank entfernen**
        frappe.db.sql("DELETE FROM `tabFile` WHERE file_url = %s", (file_url,))
        frappe.db.commit()
    except Exception:
        pass

    # **Finale Abschlussmeldung mit Dateinamen**
    return {
        "status": "success",
        "message": f"✅ Import abgeschlossen\n➕ {created_members} hinzugefügt\n🔄 {updated_members} aktualisiert\n⚠️ {ignored_members} ignoriert.\n🗑️ Datei '{deleted_file_name}' wurde gelöscht.",
        "created": created_members,
        "updated": updated_members,
        "ignored": ignored_members
    }
