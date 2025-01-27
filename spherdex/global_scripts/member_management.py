import frappe

def reset_series(prefix):
    """Setzt die Seriennummer für ein Präfix auf 0."""
    frappe.db.sql(
        "UPDATE `tabSeries` SET `current` = 0 WHERE `name` = %s",
        (prefix,)
    )

def rebuild_database_with_temp(new_prefix, new_format, renumber=False):
    """Leert die Haupttabelle und baut sie basierend auf einer temporären Tabelle neu auf."""

    # Schritt 1: Temporäre Tabelle erstellen und Mitglieder sichern
    frappe.db.sql("""
        CREATE TEMPORARY TABLE IF NOT EXISTS temp_members AS
        SELECT 
            name, vorname, nachname, geburtstag, eintrittsdatum, status, 
            austrittsdatum, adresse, handy, festnetz, mail_privat, rollen_werte, seriennummer
        FROM `tabMitglied`
        ORDER BY seriennummer ASC
    """)

    # Schritt 2: Tabelle leeren
    frappe.db.sql("DELETE FROM `tabMitglied`")

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
        return

    start_number = 1
    last_serial = 0

    for idx, member in enumerate(temp_members, start=start_number):
        serial_number = idx if renumber else member["seriennummer"]

        # Lücken prüfen und Demo-Mitglieder nur bei renumber=False anlegen
        if not renumber:
            while serial_number > last_serial + 1:
                last_serial += 1
                # Lücke gefunden, Demo-Mitglied anlegen
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

            # Überspringe die Erstellung des regulären Mitglieds, wenn die Seriennummer bereits gefüllt wurde
            if serial_number <= last_serial:
                continue

        # Neues Mitglied erstellen (virtuell)
        new_member = frappe.new_doc("Mitglied")
        new_member.update({
            "vorname": member["vorname"] or "Demo",
            "nachname": member["nachname"] or "Mitglied",
            "geburtstag": member["geburtstag"] or "1900-01-01",
            "eintrittsdatum": member["eintrittsdatum"] or "1900-01-01",
            "status": member["status"] or "Aktiv",
            "austrittsdatum": member["austrittsdatum"],
            "adresse": member["adresse"],
            "handy": member["handy"],
            "festnetz": member["festnetz"],
            "mail_privat": member["mail_privat"],
            "rollen_werte": member["rollen_werte"],
            "seriennummer": serial_number
        })
        new_member.save()

        last_serial = serial_number

    # Schritt 5: Temporäre Tabelle löschen
    frappe.db.sql_ddl("DROP TEMPORARY TABLE IF EXISTS temp_members")

    # Schritt 6: Demo-Mitglieder löschen (nur bei renumber=False)
    if not renumber:
        demo_members = frappe.get_all("Mitglied", filters={"vorname": "Demo"}, fields=["name"])
        for demo in demo_members:
            frappe.delete_doc("Mitglied", demo.name)

@frappe.whitelist()
def renumber_members():
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    rebuild_database_with_temp(settings.nummer_praefix, settings.nummer_format, renumber=True)

@frappe.whitelist()
def update_prefix(new_prefix):
    if not new_prefix:
        frappe.throw("Das neue Präfix darf nicht leer sein.")
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    rebuild_database_with_temp(new_prefix, settings.nummer_format, renumber=False)

@frappe.whitelist()
def update_prefix_and_number(new_prefix):
    if not new_prefix:
        frappe.throw("Das neue Präfix darf nicht leer sein.")
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    rebuild_database_with_temp(new_prefix, settings.nummer_format, renumber=True)

@frappe.whitelist()
def apply_new_format(new_format):
    if not new_format:
        frappe.throw("Das neue Format darf nicht leer sein.")
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    rebuild_database_with_temp(settings.nummer_praefix, new_format, renumber=False)

@frappe.whitelist()
def delete_all_members():
    frappe.db.sql("DELETE FROM `tabMitglied`")
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    reset_series(settings.nummer_praefix)

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
