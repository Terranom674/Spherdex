import frappe, re
from frappe.model.naming import getseries
from frappe.utils import cint

@staticmethod
def get_serie_length(format_string):
    """Bestimmt die Anzahl der Stellen basierend auf den Platzhaltern #"""
    match = re.search(r"<(#+)>", format_string)
    if match:
        return len(match.group(1))
    frappe.throw("Das Format muss den Platzhalter <####> enthalten.")
      
# Seriennummer generieren basierend auf Präfix
def get_serial(PREFIX,STARTNUMMER,SERIES_LENGTH):
    SERIENNUMMER = get_current_series(PREFIX)
    # Seriennummer prüfen und anpassen
    if cint(SERIENNUMMER) < STARTNUMMER:
        frappe.db.sql("UPDATE `tabSeries` SET `current` = %s WHERE `name` = %s", (STARTNUMMER-1, PREFIX,))
    #frappe.db.sql("""UPDATE `tabSeries` SET `current` = %s WHERE `name` = %s""",(1, prefix))
    return(getseries(PREFIX, SERIES_LENGTH))

def get_current_series(PREFIX):
    return(frappe.db.get_value("Series", PREFIX, "current", order_by="name"))