import frappe

@frappe.whitelist()
def get_dynamic_roles():
    """
    Lade die Rollen aus den Mitgliedereinstellungen.
    Gibt eine Liste der Rollen zurück.
    """
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    if settings.rollen:
        return [role.rollenname for role in settings.rollen]
    return []
    
@frappe.whitelist()
def get_display_mode():
    """
    Gibt den ausgewählten Anzeigemodus (MultiSelect oder Checkbox) zurück.
    """
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    return settings.rollen_anzeige