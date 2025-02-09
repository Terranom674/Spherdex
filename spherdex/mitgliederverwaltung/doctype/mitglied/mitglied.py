# Copyright (c) 2025, Thomas Dannenberg and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate
from frappe.model.naming import getseries
from ....global_scripts import initialen, serial
import json, os, datetime, tempfile, time, csv
from frappe.utils.file_manager import save_file
from frappe import _

class Mitglied(Document):
    def autoname(self):
        """Generiert die Mitgliedsnummer basierend auf den Einstellungen"""
        SETTINGS = frappe.get_single("Mitgliederverwaltung Einstellungen")

        # Präfix und Format aus den Einstellungen
        PREFIX = SETTINGS.nummer_praefix or "UNB"
        FORMAT_STRING = SETTINGS.nummer_format or "<YY><Initialen><MM><####>"
        STARTNUMMER = SETTINGS.start_nummer or 1

        # Eintrittsdatum prüfen und konvertieren
        if not self.eintrittsdatum:
            frappe.throw("Eintrittsdatum muss angegeben werden.")
        EINTRITTSDATUM = getdate(self.eintrittsdatum)
        YEAR = EINTRITTSDATUM.strftime("%y")  # Zwei Ziffern des Jahres
        FULL_YEAR = EINTRITTSDATUM.strftime("%Y")  # Volles Jahr
        MONTH = EINTRITTSDATUM.strftime("%m")  # Monat
        DAY = EINTRITTSDATUM.strftime("%d")  # Tag

        # Initialen generieren
        INITIALEN = initialen.get_initialen(self.vorname, self.nachname)

        # Laufende Nummer basierend auf Präfix
        SERIES_LENGTH = serial.get_serie_length(FORMAT_STRING)

        # Seriennummer generieren basierend auf Präfix
        SERIENNUMMER = serial.get_serial(PREFIX, STARTNUMMER, SERIES_LENGTH)

        # Seriennummer ins Hidden Field schreiben
        self.seriennummer = int(SERIENNUMMER)

        # Formatlänge anpassen
        LENGTH = ""
        count = 0
        while count < SERIES_LENGTH:
            LENGTH += "#"
            count += 1

        # Nummer zusammensetzen
        self.name = f"{PREFIX}-"+(
            FORMAT_STRING
            .replace("<YY>", YEAR)
            .replace("<YYYY>", FULL_YEAR)
            .replace("<MM>", MONTH)
            .replace("<DD>", DAY)
            .replace("<Initialen>", INITIALEN)
            .replace(f"<{LENGTH}>", SERIENNUMMER)
        )