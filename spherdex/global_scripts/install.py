import frappe

def after_install():
    # Prüfen, ob "Mitgliederverwaltung Einstellungen" existiert
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    
    # Standardwert nur setzen, wenn das Feld leer ist
    if not settings.default_anzeigenmodus:
        settings.default_anzeigenmodus = "Checkbox"
        settings.save()
        frappe.db.commit()