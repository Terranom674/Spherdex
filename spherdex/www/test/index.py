import frappe
from spherdex.utils.html_import import get_page_context

def get_context(context):
    """Lädt die Startseite `index.html` und behandelt Spezialanfragen."""
    return get_page_context(context, "index.html")
