import frappe

@frappe.whitelist()
def install_standard_roles():
    # Definiere die Standardrollen und ihre Beschreibungen
    standard_roles = [
        {"rollenname": "Vorsitzende(r)", "beschreibung": "Leitet den Verein und trägt die Hauptverantwortung."},
        {"rollenname": "stellvertretende(r) Vorsitzende(r)", "beschreibung": "Unterstützt den Vorsitzenden und übernimmt Aufgaben bei Abwesenheit."},
        {"rollenname": "Kassenwart(in)", "beschreibung": "Verantwortlich für die Buchhaltung und Finanzen."},
        {"rollenname": "Schriftführer(in)", "beschreibung": "Führt Protokolle und verwaltet wichtige Dokumente."}
    ]

    # Iteriere über die Standardrollen und prüfe, ob sie existieren
    for role in standard_roles:
        if not frappe.db.exists("Mitgliederrolle", {"rollenname": role["rollenname"]}):
            # Rolle hinzufügen, wenn sie nicht existiert
            new_role = frappe.get_doc({
                "doctype": "Mitgliederrolle",
                "rollenname": role["rollenname"],
                "beschreibung": role["beschreibung"]
            })
            new_role.insert(ignore_permissions=True)

    frappe.msgprint("Standardrollen erfolgreich installiert.")