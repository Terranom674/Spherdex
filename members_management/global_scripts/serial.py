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
    
def what_to_do(CURRENT,entry,PREFIX):
    ENTRY_SERIAL = entry.name #Zählung implementieren
    
    if ENTRY_SERIAL == CURRENT and ENTRY_SERIAL > 1:
       frappe.db.sql("UPDATE `tabSeries` SET `current` = `current` - 1 WHERE `name`= %s", PREFIX)
       return(f"Die aktuelle Seriennummer wurde auf {int(CURRENT)-1} geändert" )
    elif ENTRY_SERIAL == 1:
       frappe.db.sql("DELETE FROM `tabSeries` WHERE `name` = %s", (PREFIX,))
       return(f"Die Serie {PREFIX} existiert nicht mehr und wurde vollständig gelöscht" )         
    elif ENTRY_SERIAL < CURRENT:
       return(f"Die aktuelle Seriennummer {CURRENT} wurde nicht geändert" )
      
def get_current_series(PREFIX):
    return(frappe.db.get_value("Series", PREFIX, "current", order_by="name"))