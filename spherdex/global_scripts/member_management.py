import frappe
from spherdex.global_scripts.utils import set_database_lock

def reset_series(prefix):
    """Setzt die Seriennummer für ein Präfix auf 0."""
    frappe.db.sql(
        "UPDATE `tabSeries` SET `current` = 0 WHERE `name` = %s",
        (prefix,)
    )

def rebuild_database_with_temp(new_prefix, new_format, renumber=False):
    """Leert die Haupttabelle und baut sie basierend auf einer temporären Tabelle neu auf."""
    
    # Explizit offene Transaktion beenden
    frappe.db.commit()
    
    # Schritt 1: Temporäre Tabelle erstellen und Mitglieder sichern
    frappe.db.sql("""
        CREATE TEMPORARY TABLE IF NOT EXISTS temp_members AS
        SELECT name, vorname, nachname, geburtstag, eintrittsdatum, status, 
            austrittsdatum, adresse, handy, festnetz, mail_privat, rollen_werte, seriennummer
        FROM `tabMitglied`
        ORDER BY seriennummer ASC
    """)

    # Schritt 2: Tabelle leeren
    frappe.db.sql("DELETE FROM `tabMitglied`")
    
    # Direkt committen, um `ImplicitCommitError` zu vermeiden
    frappe.db.commit()

    # Schritt 3: Einstellungen aktualisieren
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    prefix = new_prefix or settings.nummer_praefix or "UNB"
    settings.nummer_praefix = prefix
    reset_series(prefix)
    settings.nummer_format = new_format
    settings.save()
    
    temp_members = frappe.db.sql("SELECT * FROM temp_members", as_dict=True)

    if not temp_members:
        frappe.db.sql_ddl("DROP TEMPORARY TABLE IF EXISTS temp_members")
        frappe.db.commit()
        return

    start_number = 1
    last_serial = 0

    for idx, member in enumerate(temp_members, start=start_number):
        serial_number = idx if renumber else member["seriennummer"]

        if not renumber:
            while serial_number > last_serial + 1:
                last_serial += 1
                new_member = frappe.new_doc("Mitglied")
                new_member.update({
                    "vorname": "Demo",
                    "nachname": f"Mitglied {last_serial}",
                    "geburtstag": "1900-01-01",
                    "eintrittsdatum": "1900-01-01",
                    "status": "Aktiv",
                    "seriennummer": last_serial,
                    "adresse": "",
                    "handy": "",
                    "festnetz": "",
                    "mail_privat": "",
                    "rollen_werte": ""
                })
                new_member.save()

            if serial_number <= last_serial:
                continue

        new_member = frappe.new_doc("Mitglied")
        new_member.update(member)
        new_member.seriennummer = serial_number
        new_member.save()
        last_serial = serial_number

    frappe.db.sql_ddl("DROP TEMPORARY TABLE IF EXISTS temp_members")
    
    # Letztes Commit, um alle Änderungen zu sichern
    frappe.db.commit()

    # ✅ Schritt 6: DEMO-Mitglieder löschen (nur wenn renumber=False)
    if not renumber:
        demo_members = frappe.get_all("Mitglied", filters={"vorname": "Demo"}, fields=["name"])
        for demo in demo_members:
            frappe.delete_doc("Mitglied", demo.name)
        frappe.db.commit()  # Sicherstellen, dass das Löschen abgeschlossen ist

@frappe.whitelist()
def renumber_members():
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    with_database_lock(settings, lambda: rebuild_database_with_temp(settings.nummer_praefix, settings.nummer_format, renumber=True))

@frappe.whitelist()
def update_prefix(new_prefix):
    if not new_prefix:
        frappe.throw("Das neue Präfix darf nicht leer sein.")
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    with_database_lock(settings, lambda: rebuild_database_with_temp(new_prefix, settings.nummer_format, renumber=False))

@frappe.whitelist()
def update_prefix_and_number(new_prefix):
    if not new_prefix:
        frappe.throw("Das neue Präfix darf nicht leer sein.")
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    with_database_lock(settings, lambda: rebuild_database_with_temp(new_prefix, settings.nummer_format, renumber=True))

@frappe.whitelist()
def apply_new_format(new_format):
    if not new_format:
        frappe.throw("Das neue Format darf nicht leer sein.")
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    with_database_lock(settings, lambda: rebuild_database_with_temp(settings.nummer_praefix, new_format, renumber=False))

@frappe.whitelist()
def delete_all_members():
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    with_database_lock(settings, _delete_members)

def _delete_members():
    frappe.db.sql("DELETE FROM `tabMitglied`")
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    reset_series(settings.nummer_praefix)

@frappe.whitelist()
def install_standard_roles():
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    with_database_lock(settings, _install_roles)

def _install_roles():
    standard_roles = [
        {"rollenname": "Vorsitzende(r)", "beschreibung": "Leitet den Verein."},
        {"rollenname": "Stellvertretende(r) Vorsitzende(r)", "beschreibung": "Unterstützt den Vorsitz."},
        {"rollenname": "Kassenwart(in)", "beschreibung": "Verwaltet die Finanzen."},
        {"rollenname": "Schriftführer(in)", "beschreibung": "Protokolliert Sitzungen."}
    ]
    for role in standard_roles:
        if not frappe.db.exists("Mitgliederrolle", {"rollenname": role["rollenname"]}):
            new_role = frappe.get_doc({
                "doctype": "Mitgliederrolle",
                "rollenname": role["rollenname"],
                "beschreibung": role["beschreibung"]
            })
            new_role.insert()

def with_database_lock(settings, operation):
    current_user = frappe.session.user
    set_database_lock("sperren", user=current_user, automatisch=True)
    try:
        operation()
    finally:
        set_database_lock("entsperren", automatisch=True)
