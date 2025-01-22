import frappe

def log(message, level="info"):
    """Protokolliert Nachrichten für Debugging-Zwecke."""
    frappe.log_error(message, title="Global Scripts Log")