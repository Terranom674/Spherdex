import frappe
from datetime import datetime

@frappe.whitelist()
def set_database_lock(status, user=None, automatisch=False):
    settings = frappe.get_single("Admin Einstellungen")
    current_user = frappe.session.user  # Aktueller Benutzer

    # ✅ Benutzer korrekt zuweisen
    if not user:
        user = current_user

    # ✅ Debug-Log zur Überprüfung des Status vor der Sperrung
    frappe.log_error(
        title="DEBUG: Vor Sperrstatus setzen",
        message=f"Status: {status}, Gesperrt: {settings.datenbank_gesperrt}, Automatisch: {settings.automatische_sperre}, Aktiver Benutzer: {settings.active_user}, Aktueller Benutzer: {current_user}"
    )

    # ✅ Manuelle Sperre bleibt aktiv, wenn kein automatischer Vorgang
    if (
        status == "entsperren"
        and settings.datenbank_gesperrt
        and not automatisch
        and current_user != settings.active_user
        and "System Manager" not in frappe.get_roles(current_user)
    ):
        return "⚠️ Manuelle Sperre bleibt aktiv."

    # ✅ Sperrstatus erst nach korrekter Zuweisung aktualisieren
    settings.datenbank_gesperrt = 1 if status == "sperren" else 0
    settings.automatische_sperre = 1 if automatisch and status == "sperren" else 0
    settings.active_user = user if status == "sperren" else None
    settings.save()

    sperrgrund = "Automatisch" if automatisch else "Manuell"

    # ✅ Sicherstellen, dass alle Werte gespeichert werden
    settings.save()

    # ✅ Debug-Log nach dem Speichern
    frappe.log_error(
        title="DEBUG: Nach Sperrstatus setzen",
        message=f"Status: {status}, Gesperrt: {settings.datenbank_gesperrt}, Automatisch: {settings.automatische_sperre}, Aktiver Benutzer: {settings.active_user}, Aktueller Benutzer: {current_user}"
    )

    # ✅ Protokollierung der Sperr-Aktion
    try:
        # Append statt direktem Insert
        settings.append("sperr_protokoll", {
            "zeitpunkt": datetime.now(),
            "aktion": "Sperre aktiviert" if status == "sperren" else "Sperre deaktiviert",
            "benutzer": user,
            "sperrgrund": sperrgrund
        })

        # Speichern, um ERPNext-Trigger auszulösen
        settings.save(ignore_permissions=True)

        # ✅ Debug-Log für das Protokoll
        frappe.log_error(
            title="DEBUG: Protokoll-Eintrag gespeichert",
            message=f"Aktuelle Anzahl Protokoll-Einträge: {len(settings.sperr_protokoll)}"
        )

    except Exception as e:
        frappe.log_error(title="Fehler beim Protokollieren", message=str(e))

    return f"🔒 {'Sperre aktiviert' if status == 'sperren' else 'Sperre deaktiviert'}."

def validate_database_lock(doc, method=None):
    exempt_doctypes = ["Admin Einstellungen", "Mitgliederverwaltung Einstellungen", "Error Log", "ToDo", "Sperr Protokoll"]

    if frappe.local.flags.ignore_validate:
        return  # ✅ Validierung überspringen, wenn Rekursionsschutz aktiv ist

    if doc.doctype in exempt_doctypes:
        return

    settings = frappe.get_single("Admin Einstellungen")

    # ✅ Ausnahme für den aktiven Benutzer
    if settings.datenbank_gesperrt:
        if frappe.session.user == settings.active_user:
            return  # ✅ Auslösender Benutzer darf Änderungen vornehmen

        frappe.throw("❌ Die Datenbank ist derzeit gesperrt. Änderungen sind nicht möglich.")

@frappe.whitelist()
def clear_protokoll():
    frappe.db.sql("DELETE FROM `tabSperr Protokoll`")
    frappe.db.commit()
    
@frappe.whitelist()
def get_protokoll(limit='Alle', page=1):
    limit = int(limit) if limit != 'Alle' else None
    page = int(page)
    offset = (page - 1) * limit if limit else 0

    total_count = frappe.db.count("Sperr Protokoll")
    total_pages = (total_count // limit) + (1 if total_count % limit > 0 else 0) if limit else 1

    entries = frappe.db.sql(f"""
        SELECT zeitpunkt, aktion, benutzer, sperrgrund
        FROM `tabSperr Protokoll`
        ORDER BY creation DESC
        {f"LIMIT {limit} OFFSET {offset}" if limit else ""}
    """, as_dict=True)

    return {
        "data": entries,
        "total_pages": total_pages,
        "current_page": page
    }
