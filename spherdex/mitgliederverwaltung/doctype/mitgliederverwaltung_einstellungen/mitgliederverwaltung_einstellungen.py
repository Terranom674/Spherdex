import frappe
from frappe.model.document import Document
from frappe.utils import cint
from ....global_scripts.member_management import (
    update_prefix,
    renumber_members,
    update_prefix_and_number,
    apply_new_format
)


class MitgliederverwaltungEinstellungen(Document):
    def validate(self):
        """Verhindert Änderungen an Startnummer oder Format ohne die Buttons zu nutzen"""
        PREFIX = self.nummer_praefix or "VER-"

        # Aktuelle Seriennummer abrufen
        current_series = cint(frappe.db.get_value("Series", PREFIX, "current", order_by="name"))

        # Überprüfen, ob die Serie verwendet wurde
        if current_series and current_series > 0:
            # Ursprungswerte abrufen
            original_settings = frappe.get_single("Mitgliederverwaltung Einstellungen")
            original_startnummer = original_settings.start_nummer
            original_format = original_settings.nummer_format

            # Änderungen verhindern
            if self.start_nummer != original_startnummer:
                frappe.throw(
                    f"Die Startnummer kann nicht geändert werden, da die Serie für {PREFIX} bereits verwendet wurde "
                    f"(aktuelle Seriennummer: {current_series}). Nutzen Sie den entsprechenden Button für Anpassungen."
                )

            if self.nummer_format != original_format:
                frappe.throw(
                    f"Das Format kann nicht geändert werden, da die Serie für {PREFIX} bereits verwendet wurde. "
                    f"Nutzen Sie den entsprechenden Button für Anpassungen."
                )

    @frappe.whitelist()
    def update_prefix_button(self, new_prefix):
        """Button-Funktion zum Ändern des Präfixes"""
        if not new_prefix:
            frappe.throw("Das neue Präfix darf nicht leer sein.")
        update_prefix(new_prefix)
        frappe.msgprint(f"Präfix erfolgreich auf '{new_prefix}' geändert.")

    @frappe.whitelist()
    def renumber_members_button(self):
        """Button-Funktion zum Neu-Durchnummerieren"""
        renumber_members()
        frappe.msgprint("Alle Mitglieder wurden erfolgreich neu durchnummeriert.")

    @frappe.whitelist()
    def update_prefix_and_number_button(self, new_prefix):
        """Button-Funktion zum Ändern des Präfixes und der Nummern"""
        if not new_prefix:
            frappe.throw("Das neue Präfix darf nicht leer sein.")
        update_prefix_and_number(new_prefix)
        frappe.msgprint(f"Präfix und Seriennummern erfolgreich auf '{new_prefix}' geändert.")

    @frappe.whitelist()
    def apply_new_format_button(self, new_format):
        """Button-Funktion zum Anwenden eines neuen Formats"""
        if not new_format:
            frappe.throw("Das neue Format darf nicht leer sein.")
        apply_new_format(new_format)
        frappe.msgprint("Neue Formatierung erfolgreich angewendet.")
