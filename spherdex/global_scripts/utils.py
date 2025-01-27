import frappe

def log(message, level="info"):
    """Protokolliert Nachrichten für Debugging-Zwecke."""
    frappe.log_error(message, title="Global Scripts Log")
    
@frappe.whitelist()
def fetch_roles():
    try:
        # Holen Sie sich das Single-Dokument für Einstellungen
        settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
        
        # Überprüfen, ob die Child-Tabelle 'rollen' Daten enthält
        rollen = frappe.get_all(
            "Mitgliederrolle",
            filters={"parent": "Mitgliederverwaltung Einstellungen"},
            fields=["name", "rollenname"]
        )
        
        if rollen:
            return rollen  # Rollen erfolgreich zurückgegeben
        else:
            return {"message": "Keine Rollen gefunden"}
    except Exception as e:
        frappe.log_error(message=str(e), title="Fehler beim Abrufen der Rollen")
        return {"error": str(e)}

@frappe.whitelist()
def get_settings():
    settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
    return {"default_anzeigenmodus": settings.default_anzeigenmodus}