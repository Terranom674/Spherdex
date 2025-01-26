import frappe
import re
from frappe.utils import getdate
from spherdex.global_scripts import serial, initialen


@frappe.whitelist()
def update_prefix(new_prefix):
    if not new_prefix:
        frappe.throw("Das neue Präfix darf nicht leer sein.")
    
    # Mitglieder aktualisieren
    members = frappe.get_all("Mitglied", fields=["name"])
    if not members:
        frappe.msgprint("Keine Mitglieder vorhanden, die aktualisiert werden können.")
        return

    for member in members:
        old_name = member.name
        updated_name = old_name.replace(old_name.split("-")[0], new_prefix, 1)
        frappe.db.set_value("Mitglied", old_name, "name", updated_name)
    
    # Doctype-Einstellung aktualisieren
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    settings.nummer_praefix = new_prefix
    settings.save()
    
    frappe.msgprint(f"Präfix erfolgreich auf '{new_prefix}' geändert.")



@frappe.whitelist()
def renumber_members():
    """Nummeriert alle Mitglieder neu durch, ohne die bestehende Struktur zu verändern."""
    members = frappe.get_all("Mitglied", fields=["name", "eintrittsdatum"], order_by="eintrittsdatum asc")
    if not members:
        frappe.msgprint("Keine Mitglieder vorhanden, die neu durchnummeriert werden können.")
        return
    
    for idx, member in enumerate(members, start=1):
        PREFIX = member.name.split("-")[0]  # Präfix extrahieren
        # Seriennummer neu setzen (4-stellig, führende Nullen)
        updated_name = f"{PREFIX}-{idx:04d}"
        frappe.db.set_value("Mitglied", member.name, "name", updated_name)
    
    frappe.msgprint("Seriennummern wurden erfolgreich neu durchnummeriert.")


@frappe.whitelist()
def update_prefix_and_number(new_prefix):
    if not new_prefix:
        frappe.throw("Das neue Präfix darf nicht leer sein.")
    
    members = frappe.get_all("Mitglied", fields=["name", "eintrittsdatum"], order_by="eintrittsdatum asc")
    if not members:
        frappe.msgprint("Keine Mitglieder vorhanden, die aktualisiert werden können.")
        return

    for idx, member in enumerate(members, start=1):
        updated_name = f"{new_prefix}-{idx:04d}"
        frappe.db.set_value("Mitglied", member.name, "name", updated_name)
    
    # Doctype-Einstellung aktualisieren
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    settings.nummer_praefix = new_prefix
    settings.start_nummer = len(members) + 1
    settings.save()
    
    frappe.msgprint(f"Präfix und Nummern wurden erfolgreich auf '{new_prefix}' aktualisiert.")



@frappe.whitelist()
def delete_all_members():
    """Löscht alle Mitglieder aus der Datenbank."""
    members = frappe.get_all("Mitglied", fields=["name"])
    if not members:
        frappe.msgprint("Es gibt keine Mitglieder, die gelöscht werden können.")
        return

    frappe.db.sql("DELETE FROM `tabMitglied`")
    frappe.msgprint("Alle Mitglieder wurden erfolgreich gelöscht.")


@frappe.whitelist()
def apply_new_format(new_format):
    """Wendet ein neues Nummernformat auf alle Mitglieder an, einschließlich Seriennummern basierend auf '#'-Platzhaltern."""
    if not new_format:
        frappe.throw("Das neue Format darf nicht leer sein.")
    
    members = frappe.get_all("Mitglied", fields=["name", "eintrittsdatum", "vorname", "nachname"], order_by="eintrittsdatum asc")
    if not members:
        frappe.msgprint("Keine Mitglieder vorhanden, die aktualisiert werden können.")
        return

    # Präfix und Startnummer aus den Einstellungen
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    prefix = settings.nummer_praefix or "UNB"
    start_number = settings.start_nummer or 1

    # Anzahl der # im Format bestimmen
    match = re.search(r"<(#+)>", new_format)
    if not match:
        frappe.throw("Das neue Format muss mindestens einen <####>-Platzhalter enthalten.")
    serial_length = len(match.group(1))  # Länge der Seriennummer basierend auf der Anzahl der #

    # Mitglieder aktualisieren
    for idx, member in enumerate(members, start=start_number):
        eintritt = getdate(member.eintrittsdatum)

        # Werte für das neue Format berechnen
        year = eintritt.strftime("%y")  # Zwei Ziffern des Jahres
        full_year = eintritt.strftime("%Y")  # Volles Jahr
        month = eintritt.strftime("%m")  # Monat
        day = eintritt.strftime("%d")  # Tag
        INITIALEN = initialen.get_initialen(member.vorname, member.nachname)  # Initialen generieren
        serial = f"{idx:0{serial_length}d}"  # Seriennummer mit der bestimmten Länge

        # Neues Format anwenden
        updated_name = f"{prefix}-"+(
            new_format
            .replace(f"<{'#' * serial_length}>", serial)  # Ersetzt die Platzhalter durch die Seriennummer
            .replace("<YY>", year)
            .replace("<YYYY>", full_year)
            .replace("<MM>", month)
            .replace("<DD>", day)
            .replace("<Initialen>", INITIALEN)
        )
        frappe.db.set_value("Mitglied", member.name, "name", updated_name)

    # Doctype-Einstellung aktualisieren
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    settings.nummer_format = new_format
    settings.save()

    frappe.msgprint("Neue Formatierung wurde erfolgreich angewendet, einschließlich aktualisierter Seriennummern.")



@frappe.whitelist()
def install_standard_roles():
    """Fügt die Standardrollen hinzu, wenn diese nicht bereits existieren."""
    standard_roles = [
        {"rollenname": "Vorsitzende(r)", "beschreibung": "Leitet den Verein und ist für strategische Entscheidungen verantwortlich."},
        {"rollenname": "Stellvertretende(r) Vorsitzende(r)", "beschreibung": "Unterstützt den Vorsitz und übernimmt Vertretungen."},
        {"rollenname": "Kassenwart(in)", "beschreibung": "Verwaltet die Finanzen und ist für die Buchhaltung zuständig."},
        {"rollenname": "Schriftführer(in)", "beschreibung": "Protokolliert Sitzungen und verwaltet Dokumente."}
    ]
    
    for role in standard_roles:
        if not frappe.db.exists("Mitgliederrolle", {"rollenname": role["rollenname"]}):
            new_role = frappe.get_doc({
                "doctype": "Mitgliederrolle",
                "rollenname": role["rollenname"],
                "beschreibung": role["beschreibung"]
            })
            new_role.insert()
    
    frappe.msgprint("Standardrollen wurden erfolgreich installiert.")
    
@frappe.whitelist()
def install_standard_roles():
    """Installiert Standardrollen in die Child-Tabelle 'Mitgliederrolle'"""
    # Parent-DocType abrufen
    einstellungen = frappe.get_doc("Mitgliederverwaltung Einstellungen", "Mitgliederverwaltung Einstellungen")
    
    # Vorhandene Rollen prüfen
    existing_roles = [row.rollenname for row in einstellungen.rollen]

    # Standardrollen definieren
    standard_roles = [
        {"rollenname": "Vorsitzende(r)", "beschreibung": "Leitet den Verein und repräsentiert ihn nach außen."},
        {"rollenname": "stellvertretende(r) Vorsitzende(r)", "beschreibung": "Unterstützt und vertritt den Vorsitzenden."},
        {"rollenname": "Kassenwart(in)", "beschreibung": "Verantwortlich für die Finanzen des Vereins."},
        {"rollenname": "Schriftführer(in)", "beschreibung": "Protokolliert die Treffen und führt die Vereinsunterlagen."}
    ]
    
    # Rollen hinzufügen, wenn sie nicht existieren
    for role in standard_roles:
        if role["rollenname"] not in existing_roles:
            einstellungen.append("rollen", role)
    
    # Änderungen speichern
    einstellungen.save()
    frappe.msgprint("Standardrollen wurden erfolgreich installiert.")