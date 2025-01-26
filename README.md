# Spherdex: Die modulare Verwaltungssoftware

<table style="width: 100%; border: none; !important">
<tr>
<td style="width: 50%; vertical-align: top; border: none; !important">
<img src="https://github.com/user-attachments/assets/1b0764aa-99d3-4a2a-a38f-33e9200ef2ba">
</td>
<td style="width: 50%; vertical-align: top; border: none; !important">

### **Inhaltsverzeichnis**
1. [Projektübersicht](#projektübersicht)
2. [Details zu den Modulen](#details-zu-den-modulen)
   - [Mitgliederverwaltung](#mitgliederverwaltung-)
   - [Veranstaltungsmanagement](#veranstaltungsmanagement-)
   - [Self-Service-Portal](#self-service-portal-)
   - [Integration mit Cloud-Diensten](#integration-mit-cloud-diensten-)
   - [Automatisierung](#automatisierung-)
   - [Finanzverwaltung](#finanzverwaltung-)
   - [Inventarverwaltung](#inventarverwaltung-)
   - [Kommunikation und Chat](#kommunikation-und-chat-)
   - [Kalender- und Terminplanung](#kalender-und-terminplanung-)
3. [Handbuch](#handbuch)
4. [FAQ](#faq)
5. [Langfristige Vision](#langfristige-vision)
6. [Changelog](#changelog)

</td>
</tr>
</table>

**Spherdex** ist eine innovative Softwarelösung zur Verwaltung von Mitgliedern, Veranstaltungen, Inventar und vielem mehr. Eine Komplettlösung für Vereine, Clubs und Verbünde.

![License: AGPL-3.0](https://img.shields.io/badge/license-AGPL--3.0-blue) 

|[![Mitgliederverwaltung: 0.5.0](https://img.shields.io/badge/Mitgliederverwaltung-0.5.0-green)](#mitgliederverwaltung-) | [Changelog](#changelog)| [Handbuch](#handbuch)| |
|---|---|---|---|
| [![Veranstaltungsmanagement: 0.0.0](https://img.shields.io/badge/Veranstaltungsmanagement-0.0.0-lightgrey)](#veranstaltungsmanagement-) | [![Self-Service-Portal: 0.0.0](https://img.shields.io/badge/Self--Service--Portal-0.0.0-lightgrey)](#self-service-portal-) | [![Cloud-Integration: 0.0.0](https://img.shields.io/badge/Cloud--Integration-0.0.0-lightgrey)](#integration-mit-cloud-diensten-) | [![Automatisierung: 0.0.0](https://img.shields.io/badge/Automatisierung-0.0.0-lightgrey)](#automatisierung-)
| [![Finanzverwaltung: 0.0.0](https://img.shields.io/badge/Finanzverwaltung-0.0.0-lightgrey)](#finanzverwaltung-) | [![Inventarverwaltung: 0.0.0](https://img.shields.io/badge/Inventarverwaltung-0.0.0-lightgrey)](#inventarverwaltung-) | [![Kommunikation: 0.0.0](https://img.shields.io/badge/Kommunikation-0.0.0-lightgrey)](#kommunikation-und-chat-) | [![Kalender: 0.0.0](https://img.shields.io/badge/Kalender-0.0.0-lightgrey)](#kalender-und-terminplanung-)

---

## **Projektübersicht**

<details>
<summary><b>Projektfortschritt anzeigen</b></summary>

Dieses Projekt umfasst folgende Module. Der Fortschritt des jeweiligen Moduls wird in Prozent angezeigt:

| Modul                           | Fortschritt                                                                 |
|-------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
|[![Mitgliederverwaltung](https://img.shields.io/badge/Mitgliederverwaltung-50%25-yellow)](#mitgliederverwaltung-)| ![50%](https://progress-bar.xyz/50?title=Mitgliederverwaltung&width=300) |
|<img src="https://github.com/user-attachments/assets/c6d55ca3-b9c5-4504-ac67-015ad67af5ff" width="48"> **[Veranstaltungsmanagement](#veranstaltungsmanagement-)**| ![0%](https://progress-bar.xyz/0?title=Veranstaltungsmanagement&width=300) |
|<img src="https://github.com/user-attachments/assets/6bd9da27-2b35-476e-b07d-561a460e0c6f" width="48"> **[Self-Service-Portal](#self-service-portal-)**| ![0%](https://progress-bar.xyz/0?title=Self-Service-Portal&width=300) |
|<img src="https://github.com/user-attachments/assets/4041d589-fb78-401a-87ea-b9b1f8ee73cc" width="48"> **[Integration mit Cloud-Diensten](#integration-mit-cloud-diensten-)**| ![0%](https://progress-bar.xyz/0?title=Cloud-Integration&width=300) |
|<img src="https://github.com/user-attachments/assets/8e904845-a574-4a9a-b1fe-724b45213eb2" width="48"> **[Automatisierung](#automatisierung-)**| ![0%](https://progress-bar.xyz/0?title=Automatisierung&width=300) |
|<img src="https://github.com/user-attachments/assets/6503df2d-0d20-403c-89d7-43eefc3fcc7b" width="48"> **[Finanzverwaltung](#finanzverwaltung-)**| ![0%](https://progress-bar.xyz/0?title=Finanzverwaltung&width=300) |
|<img src="https://github.com/user-attachments/assets/f74e0778-bd02-48cb-8beb-d4896227a8da" width="48"> **[Inventarverwaltung](#inventarverwaltung-)**| ![0%](https://progress-bar.xyz/0?title=Inventarverwaltung&width=300) |
|<img src="https://github.com/user-attachments/assets/0eccb399-abd4-454f-8f12-180ec7ebf984" width="48"> **[Kommunikation und Chat](#kommunikation-und-chat-)**| ![0%](https://progress-bar.xyz/0?title=Kommunikation&width=300) |
|<img src="https://github.com/user-attachments/assets/59e248f2-9fc2-403d-96ac-3431c924d56d" width="48"> **[Kalender- und Terminplanung](#kalender-und-terminplanung-)**| ![0%](https://progress-bar.xyz/0?title=Kalenderplanung&width=300) |

</details>

---

## **Details zu den Modulen**

### **Mitgliederverwaltung** <img src="https://github.com/user-attachments/assets/95d988ab-7d1a-45bd-b20e-518f31e6ee34" width="48">
<details>
<summary><b>Details</b></summary>
Die Mitgliederverwaltung ist das zentrale Modul von Spherdex und bietet umfassende Funktionen zur Erfassung und Organisation von Mitgliedern.

**Aktuell verfügbare Funktionen:**
- <ins>Mitglieder-Datenverwaltung</ins>: Verwaltung von persönlichen Daten wie Vorname, Nachname, Geburtstag und Kontaktinformationen. ![Umgesetzt](https://img.shields.io/badge/Umgesetzt-green)
- <ins>Rollenverwaltung</ins>: Zuweisung von Rollen wie Vorsitzender, Schatzmeister oder Mitglied. ![Umgesetzt](https://img.shields.io/badge/Umgesetzt-green) 
- <ins>Präfix- und Nummernänderung</ins>: Anpassung des Präfixes und der laufenden Nummer für Mitgliedsnummern. ![Umgesetzt](https://img.shields.io/badge/Umgesetzt-green) 
- <ins>MultiSelect/Checkbox für Rollen</ins>: Auswahl und Anzeige von Rollen als Checkboxen oder in einem Dropdown-Menü, inklusive Synchronisierung und Speicherung. ![Umgesetzt](https://img.shields.io/badge/Umgesetzt-green)
- <ins>Beitragsverwaltung</ins>: Verwaltung und Nachverfolgung von Mitgliedsbeiträgen und offenen Zahlungen. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- <ins>Berichte und Statistiken</ins>: Erstellung von Analysen und Übersichten zur Mitgliedschaft und Beitragszahlungen. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- <ins>Geburtstagsbenachrichtigung</ins>: Automatischer Versand von Geburtstagsgrüßen per E-Mail. ![In Entwicklung](https://img.shields.io/badge/In_Entwicklung-yellow)
- <ins>Datenimport/-export</ins>: Import und Export von Mitgliedsdaten in Formaten wie PDF, CSV, TXT, DOC und Excel. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)

Dieses Modul bildet die Grundlage für weitere Erweiterungen und ermöglicht eine präzise Verwaltung aller Vereinsmitglieder.
</details>

<details>
<summary><b>Roadmap</b></summary>

#### Aktueller Stand
- **Version:** 0.5.0
- **Status:** In aktiver Entwicklung
- **Ziel:** Stabilisierung und Vorbereitung für Version 1.0.0.

#### Fortschritt
| Funktion                          | Status                  | Fortschritt                                                                 |
|-----------------------------------|-------------------------|-----------------------------------------------------------------------------|
| **Mitglieder-Datenverwaltung**    | **Umgesetzt**           | ![100%](https://progress-bar.xyz/100?title=Datenverwaltung&width=300)      |
| **Rollenverwaltung**              | **Umgesetzt**           | ![100%](https://progress-bar.xyz/100?title=Rollenverwaltung&width=300)     |
| **Präfix- und Nummernänderung**   | **Umgesetzt**           | ![100%](https://progress-bar.xyz/100?title=Pr%C3%A4fix-%26-Nummerierung&width=300) |
| **MultiSelect/Checkbox für Rollen** | **Umgesetzt**          | ![100%](https://progress-bar.xyz/100?title=MultiSelect-%2F-Checkbox&width=300) |
| **Beitragsverwaltung**            | **Geplant**             | ![0%](https://progress-bar.xyz/0?title=Beitragsverwaltung&width=300)       |
| **Berichte und Statistiken**      | **Geplant**             | ![0%](https://progress-bar.xyz/0?title=Berichte+%26+Statistiken&width=300) |
| **Geburtstagsbenachrichtigung**   | **In Entwicklung**      | ![10%](https://progress-bar.xyz/10?title=Geburtstagsbenachrichtigung&width=300) |
| **Datenimport/-export**           | **Geplant**             | ![0%](https://progress-bar.xyz/0?title=Datenimport-Export&width=300)       |

#### Funktionen im Detail

#### 1. Mitglieder-Datenverwaltung
- Speicherung persönlicher Daten (Vorname, Nachname, Geburtstag, Kontaktinformationen).
- Verwaltung von Mitgliedsstatus (Aktiv, Passiv, Gekündigt).

#### 2. Rollenverwaltung
- Zuweisung von Rollen wie Vorsitzender oder Schatzmeister.
- Unterstützung von Checkboxen und MultiSelect zur Darstellung der Rollen.

#### 3. Präfix- und Nummernänderung
- Anpassung des Präfixes und der laufenden Nummer für alle Mitglieder.

#### 4. MultiSelect/Checkbox für Rollen
- Endanwender kann zwischen einer Checkbox-Darstellung und einer MultiSelect-Darstellung wählen.

#### 5. Beitragsverwaltung
- Automatische Erstellung und Verwaltung von Mitgliedsbeiträgen.
- Nachverfolgung offener Zahlungen.

#### 6. Berichte und Statistiken
- Erstellung von Statistiken und Analysen zur Mitgliedschaft und Beitragszahlungen.

#### 7. Geburtstagsbenachrichtigung
- Automatische E-Mail-Benachrichtigung an Mitglieder an deren Geburtstag.

#### 8. Datenimport/-export
- **Formate für den Export:** PDF, CSV, TXT, DOC und Excel.
- **Funktionen:** 
  - Export aller Mitgliedsdaten oder nach Filterkriterien.
  - Import von Daten aus CSV und Excel.
  - Validierung der Daten beim Import.
    
#### 9. Optimierung und Debuggung

#### Ziel für Version 1.0.0
- Vollständige Umsetzung aller geplanten Funktionen.
- Testen und Stabilisieren des Moduls.
- Vorbereitung für Integration mit anderen Modulen.
</details>

### **Veranstaltungsmanagement** <img src="https://github.com/user-attachments/assets/c6d55ca3-b9c5-4504-ac67-015ad67af5ff" width="48">
<details>
   <summary><b>Details</b></summary>

   Das Veranstaltungsmanagement bietet Werkzeuge zur Organisation:
- Veranstaltungsplanung: Erstellen und Verwalten von Events, Proben und Auftritten. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- Teilnehmerlisten: Übersicht über bestätigte Teilnehmer. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- Budgetverwaltung: Einnahmen- und Ausgabenkontrolle. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- Feedback: Analyse von Veranstaltungsbewertungen. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)

</details>

<details>
<summary><b>Roadmap</b></summary>
Folgt bald
</details>

### **Self-Service-Portal** <img src="https://github.com/user-attachments/assets/6bd9da27-2b35-476e-b07d-561a460e0c6f" width="48">
<details>
   <summary><b>Details</b></summary>

   Das Self-Service-Portal ermöglicht:
- Datenzugriff: Mitglieder können ihre persönlichen Informationen einsehen und bearbeiten. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- Dashboards: Individualisierbare Übersicht für Mitglieder. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- Zugriff auf Dokumente:** Mitglieder können Rechnungen und Bescheinigungen herunterladen.![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
</details>

<details>
<summary><b>Roadmap</b></summary>
Folgt bald
</details>

### Integration mit Cloud-Diensten <img src="https://github.com/user-attachments/assets/4041d589-fb78-401a-87ea-b9b1f8ee73cc" width="48">
<details>
   <summary><b>Details</b></summary>

   Dieses Modul integriert die Software nahtlos mit Cloud-Lösungen:
- Dateiverwaltung: Automatische Synchronisation mit Nextcloud. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- Benutzerverwaltung: Erstellung von Cloud-Accounts direkt über die Software. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- Automatische Backups: Regelmäßige Sicherung von Daten in der Cloud. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
</details>

<details>
<summary><b>Roadmap</b></summary>
Folgt bald
</details>

### Automatisierung <img src="https://github.com/user-attachments/assets/8e904845-a574-4a9a-b1fe-724b45213eb2" width="48">
<details>
   <summary><b>Details</b></summary>

   Automatisierung reduziert manuellen Aufwand:
- Benachrichtigungen:** Erinnerungen zu Geburtstagen, Zahlungen und Fristen. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- Zeitgesteuerte Aktionen:** Versand von Nachrichten und Reports zu festgelegten Zeiten. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
-  Workflows:** Automatische Abläufe für häufige Aufgaben. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
</details>

<details>
<summary><b>Roadmap</b></summary>
Folgt bald
</details>

### Finanzverwaltung <img src="https://github.com/user-attachments/assets/6503df2d-0d20-403c-89d7-43eefc3fcc7b" width="48">
<details>
   <summary><b>Details</b></summary>

   Die Finanzverwaltung bietet:
- Einnahmen und Ausgaben: Detaillierte Nachverfolgung aller finanziellen Aktivitäten. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- Spendenmanagement: Erstellung und Verwaltung von Spendenquittungen. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- Berichte: Steuerkonforme Jahresabschlüsse. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
</details>

<details>
<summary><b>Roadmap</b></summary>
Folgt bald
</details>

### Inventarverwaltung <img src="https://github.com/user-attachments/assets/f74e0778-bd02-48cb-8beb-d4896227a8da" width="48"> 
<details>
   <summary><b>Details</b></summary>

   Dieses Modul hilft bei der Verwaltung von Ressourcen:
- Materialübersicht: Bestandsverwaltung von Technik, Kostümen und Materialien. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- Reservierungen: Zuweisung von Ressourcen zu Veranstaltungen. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- Bestandswarnungen: Automatische Benachrichtigungen bei niedrigem Bestand. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
</details>

<details>
<summary><b>Roadmap</b></summary>
Folgt bald
</details>

### Kommunikation und Chat <img src="https://github.com/user-attachments/assets/0eccb399-abd4-454f-8f12-180ec7ebf984" width="48">
<details>
   <summary><b>Details</b></summary>

   Das Modul Kommunikation und Chat ermöglicht: 
- Interne Kommunikation: Nachrichten und Diskussionen innerhalb des Teams. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- Broadcast-Nachrichten: Einfache Kommunikation mit allen Mitgliedern. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- E-Mail-Integration: Versand von Benachrichtigungen direkt aus der Software. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
</details>

<details>
<summary><b>Roadmap</b></summary>
Folgt bald
</details>

### Kalender- und Terminplanung <img src="https://github.com/user-attachments/assets/59e248f2-9fc2-403d-96ac-3431c924d56d" width="48">
<details>
   <summary><b>Details</b></summary>

   Zur Optimierung von Zeitplänen:
- Kalendersynchronisation: Verbindung mit externen Kalenderdiensten. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- Gruppenkalender: Übersicht über gemeinsame Termine. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- Erinnerungen: Automatische Benachrichtigungen zu wichtigen Terminen. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
</details>

<details>
<summary><b>Roadmap</b></summary>
Folgt bald
</details>

---

## **Langfristige Vision**

<details>
<summary><b>1. Modularität und Erweiterbarkeit</b></summary>
Spherdex soll ein vollständig modulares System werden, das beliebig erweitert und individuell an die Anforderungen von Vereinen, Clubs und Organisationen angepasst werden kann.
</details>

<details>
<summary><b>2. Integration mit anderen Plattformen</b></summary>
Durch API-Unterstützung und Cloud-Integrationen sollen Daten und Prozesse nahtlos mit anderen Tools verbunden werden können.
</details>

<details>
<summary><b>3. Benutzerfreundlichkeit</b></summary>
Die Benutzeroberfläche wird kontinuierlich optimiert, um eine einfache Bedienung ohne tiefgehende technische Vorkenntnisse zu gewährleisten.
</details>

<details>
<summary><b>4. Automatisierung und Intelligenz</b></summary>
Durch KI-gestützte Features, wie automatische Erinnerungen und Analysen, soll Spherdex den Verwaltungsaufwand weiter reduzieren.
</details>

<details>
<summary><b>5. Skalierbarkeit</b></summary>
Die Software wird so entwickelt, dass sie für kleine Vereine genauso geeignet ist wie für größere Organisationen mit komplexen Strukturen.
</details>

<details>
<summary><b>6. Community-Engagement</b></summary>
Eine aktive Community wird gefördert, um Ideen und Feedback auszutauschen, neue Features zu entwickeln und die Software weiter voranzutreiben.
</details>

---

## **FAQ**

<details>
<summary><b>1. Was ist Spherdex?</b></summary>
Spherdex ist eine modulare Softwarelösung zur Verwaltung von Mitgliedern, Veranstaltungen, Finanzen, Inventar und mehr – ideal für Vereine, Clubs und ähnliche Organisationen.
</details>

<details>
<summary><b>2. Ist Spherdex kostenlos?</b></summary>
Ja, Spherdex ist kostenfrei und bleibt es auch in der Basisversion. Einige erweiterte Funktionen oder Module könnten jedoch in Zukunft kostenpflichtig werden, um die entstehenden Entwicklungs- und Betriebskosten zu decken. Dies betrifft beispielsweise Premium-Features oder spezielle Integrationen, die über den grundlegenden Funktionsumfang hinausgehen.
</details>

<details>
<summary><b>3. Welche Module gibt es derzeit?</b></summary>
Aktuell wird die Mitgliederverwaltung (Version 0.4.1) entwickelt. Weitere Module wie Veranstaltungsmanagement, Finanzverwaltung und Inventarverwaltung sind in Planung.
</details>

<details>
<summary><b>4. Kann ich Spherdex anpassen?</b></summary>
Ja, Spherdex ist so gestaltet, dass es leicht an spezifische Anforderungen angepasst werden kann. Entwickler können eigene Module hinzufügen oder bestehende Module erweitern.
</details>

<details>
<summary><b>5. Wird Support angeboten?</b></summary>
Da Spherdex Open Source ist, erfolgt der Support durch die Community. In der Zukunft ist ein Forum oder ein Wiki für häufige Fragen und Antworten geplant.
</details>

<details>
<summary><b>6. Welche technischen Voraussetzungen gibt es?</b></summary>
Spherdex basiert auf Frappe/ERPNext und benötigt eine entsprechende Serverumgebung. Eine detaillierte Installationsanleitung ist in Arbeit.
</details>

<details>
<summary><b>7. Gibt es eine API für Spherdex?</b></summary>
Eine API ist in Planung und wird in zukünftigen Versionen implementiert, um Integrationen mit anderen Systemen zu erleichtern.
</details>

<details>
<summary><b>8. Kann ich mehrere Module gleichzeitig nutzen?</b></summary>
Ja, sobald die Module verfügbar sind, können sie beliebig kombiniert und eingesetzt werden. Jedes Modul ist eigenständig, die Mitgliederverwaltung ist jedoch Voraussetzung.
</details>

<details>
<summary><b>9. Wird Spherdex regelmäßig aktualisiert?</b></summary>
Ja, regelmäßige Updates und neue Funktionen sind geplant, um die Software kontinuierlich zu verbessern.
</details>

<details>
<summary><b>10. Wie kann ich zur Entwicklung beitragen?</b></summary>
Sie können zur Entwicklung beitragen, indem Sie Vorschläge einreichen, Code beisteuern oder die Software testen. Mehr Informationen dazu folgen bald.
</details>

--- 

## Handbuch
Eine umfassende Dokumentation ist in Arbeit. Es wird:
- Anleitungen zur Konfiguration und Nutzung der Module enthalten.
- Beispiele und Anwendungsfälle beschreiben.
- In einem einfach zugänglichen Format (z. B. PDF, Online-Link oder direkt in der README.md) bereitgestellt

<details>
<summary><b>Roadmap</b></summary>

| Bereich                         | Fortschritt                                                                 |
|---------------------------------|-----------------------------------------------------------------------------|
| **Installationsanleitung**      | ![0%](https://progress-bar.xyz/0?title=Installationsanleitung&width=300)   |
| **Erste Schritte**              | ![0%](https://progress-bar.xyz/0?title=Erste+Schritte&width=300)           |
| **Benutzerhandbuch**            | ![0%](https://progress-bar.xyz/0?title=Benutzerhandbuch&width=300)         |
| **Entwicklerhandbuch**          | ![0%](https://progress-bar.xyz/0?title=Entwicklerhandbuch&width=300)       |
| **API-Dokumentation**           | ![0%](https://progress-bar.xyz/0?title=API-Dokumentation&width=300)        |
| **Fehlerbehebung und Support**  | ![0%](https://progress-bar.xyz/0?title=Fehlerbehebung+und+Support&width=300) |

### Installationsanleitung
- Detaillierte Schritte zur Installation der Software. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- Fehlerbehebung bei Installationsproblemen. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)

### Erste Schritte
- Einführung in die Benutzeroberfläche und Grundfunktionen. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- Anleitungen zur ersten Konfiguration. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)

### Benutzerhandbuch
- Ausführliche Beschreibung der Module und Funktionen. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- Empfehlungen für die optimale Nutzung. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)

### Entwicklerhandbuch
- Leitfäden für Entwickler zur Erweiterung der Software. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
- Beispiele für API- und Modulnutzung. ![Geplant](https://img.shields.io/badge/Geplant-lightgrey)
</details>

---

## Changelog

<details>
<summary><b>Version 0.5.0</b></summary>

   - ![Neu](https://img.shields.io/badge/Neu-Announcement-brightgreen) Fertigstellung der MultiSelect-/Checkbox-Funktionalität mit Synchronisierung und Speicherung.
   - ![Behoben](https://img.shields.io/badge/Behoben-Bugfix-blue) Fehler bei der Anzeige und Speicherung von Rollen wurden behoben.
   - ![Neu](https://img.shields.io/badge/Neu-Feature-brightgreen) Verbesserung der Sichtbarkeitssteuerung basierend auf den Einstellungen.
   - ![Optimierung](https://img.shields.io/badge/Optimierung-Improvement-yellow) Code-Struktur verbessert und Datenflüsse optimiert.

</details>


<details>
<summary><b>Version 0.4.1</b></summary>

   - ![Neu](https://img.shields.io/badge/Neu-Announcement-brightgreen) Beispielrollen werden jetzt korrekt installiert.
   - ![Behoben](https://img.shields.io/badge/Behoben-Bugfix-blue) Das Feld "Standard Rollen-Anzeigemodus" hat nach der Installation keinen Standardwert angezeigt.

</details>

<details>
<summary><b>Version 0.4.0</b></summary>

   - ![Neu](https://img.shields.io/badge/Neu-Feature-brightgreen) Die Mitgliederverwaltung wurde implementiert.
   - ![Geändert](https://img.shields.io/badge/Ge%C3%A4ndert-Update-yellow) Die Präfix- und Nummernänderung wurde erweitert.
   - ![Behoben](https://img.shields.io/badge/Behoben-Bugfix-blue) Fehler bei der Sortierung der Mitgliederliste wurde behoben.

</details>

<details>
<summary><b>Version 0.3.0</b></summary>

   - ![Neu](https://img.shields.io/badge/Neu-Feature-brightgreen) Einführung der Rollenverwaltung für Mitglieder.
   - ![Geändert](https://img.shields.io/badge/Ge%C3%A4ndert-Update-yellow) Anpassung der Datenbankstruktur für bessere Performance.
   - ![Behoben](https://img.shields.io/badge/Behoben-Bugfix-blue) Fehler in der API-Dokumentation behoben.

</details>

<details>
<summary><b>Version 0.2.0</b></summary>

   - ![Neu](https://img.shields.io/badge/Neu-Feature-brightgreen) Einführung der Präfix- und Seriennummernverwaltung.
   - ![Behoben](https://img.shields.io/badge/Behoben-Bugfix-blue) Probleme mit der Mitglieder-Datenbank wurden behoben.

</details>

<details>
<summary><b>Version 0.1.0</b></summary>

   - ![Neu](https://img.shields.io/badge/Neu-Feature-brightgreen) Erstes Release mit grundlegenden Funktionen.
   - ![Neu](https://img.shields.io/badge/Neu-Feature-brightgreen) Unterstützung für die Verwaltung persönlicher Daten (Vorname, Nachname, Geburtstag).
   - ![Behoben](https://img.shields.io/badge/Behoben-Bugfix-blue) Erste Fehlerkorrekturen nach dem initialen Release.

</details>
