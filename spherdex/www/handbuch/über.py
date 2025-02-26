import frappe
from spherdex.utils.html_import import get_page_context

def get_context(context):
    return get_page_context(context, "über.html")
