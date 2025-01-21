# Copyright (c) 2025, Thomas Dannenberg and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cint


class MitgliederverwaltungEinstellungen(Document):
    def validate(self):
        """Verhindert das Ändern der Startnummer, wenn die Serie bereits existiert"""
        PREFIX = self.nummer_praefix or "VER-"

        # Abrufen der aktuellen Seriennummer
        current_series = cint(frappe.db.get_value("Series", PREFIX, "current", order_by="name"))

        # Überprüfen, ob die Serie verwendet wurde
        if current_series and current_series > 0:
            # Abrufen der ursprünglichen Startnummer
            original_startnummer = frappe.get_single("Mitgliederverwaltung Einstellungen").start_nummer
            if self.start_nummer != original_startnummer:
                frappe.throw(
                    f"Die Startnummer kann nicht geändert werden, da die Serie für {PREFIX} bereits verwendet wurde "
                    f"(aktuelle Seriennummer: {current_series})."
                )
            # Abrufen des ursprünglichen Format
            original_format = frappe.get_single("Mitgliederverwaltung Einstellungen").nummer_format
            if self.nummer_format != original_format:
                frappe.throw(
                    f"Das Format kann nicht geändert werden, da die Serie für {PREFIX} bereits verwendet wurde "
                )
                
                
                