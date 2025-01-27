import frappe

def execute():
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    if not settings.default_anzeigenmodus:
        settings.default_anzeigenmodus = "Checkbox"
        settings.save()
        frappe.db.commit()