# Installation von Spherdex

## 1. Einleitung

ERPNext ist ein Open-Source-ERP-System, das verschiedene Geschäftsprozesse, wie Mitgliederverwaltung, Buchhaltung und Bestandsverwaltung, abdeckt. Spherdex baut auf ERPNext auf und erweitert es für die spezifischen Bedürfnisse von Vereinen und Verbänden. Diese Anleitung beschreibt, wie du Spherdex installierst und in Betrieb nimmst. Die Schritte sind so gestaltet, dass auch Nutzer mit wenig Vorkenntnissen sie nachvollziehen können.
Diese Anleitung beschreibt die Installation von **Spherdex** auf einem Ubuntu-Server mit **Frappe Bench** und **Supervisor**. Sie richtet sich an Administratoren und Entwickler, die eine stabile und sichere Umgebung für den Betrieb von Spherdex aufsetzen möchten.

## 2. Systemanforderungen
### Hardware-Anforderungen
- **CPU**: Mindestens 2 vCPUs (empfohlen: 4 vCPUs)
- **RAM**: Mindestens 4 GB (empfohlen: 8 GB oder mehr)
- **Speicher**: Mindestens 40 GB SSD (mehr für größere Datenmengen)

### Software-Anforderungen
- **Ubuntu 24.04 LTS**
- **Python 3.11+**
- **pip 20+**
- **MariaDB 10.3+**
- **Node.js 18**
- **Yarn 1.12+**
- **Redis** für Caching
- **Supervisor** für Prozessmanagement
- **Nginx** als Webserver

## 3. Vorbereitung

Bevor wir mit der Installation beginnen, müssen wir sicherstellen, dass alle notwendigen Pakete installiert und das System korrekt eingerichtet ist. Dazu gehören das Anlegen eines neuen Benutzers, das Installieren von Abhängigkeiten und die Konfiguration der Datenbank.
### Pakete aktualisieren
Aktualisiere zunächst die Paketlisten und installiere verfügbare Updates:
```bash
sudo apt-get update -y && sudo apt-get upgrade -y
```

### Neuen Benutzer erstellen

Es ist wichtig, einen separaten Benutzer für die Installation zu verwenden, um Sicherheits- und Berechtigungsprobleme zu vermeiden. Dieser Benutzer wird für die Verwaltung von Frappe Bench genutzt.
Erstelle einen separaten Benutzer für die Installation, um Berechtigungsprobleme zu vermeiden:
```bash
sudo adduser [frappe-user]
sudo usermod -aG sudo [frappe-user]
su - [frappe-user]
cd /home/[frappe-user]
```

### Notwendige Pakete installieren
Installiere alle erforderlichen Pakete für die Umgebung:
```bash
sudo apt-get install -y git python3-dev python3-setuptools python3-pip python3.12-venv \
    mariadb-server redis-server curl npm supervisor nginx \
    xvfb libfontconfig wkhtmltopdf
```

### MariaDB konfigurieren
Setze die MariaDB-Datenbank sicher auf:
```bash
sudo mysql_secure_installation
```
Folgende Einstellungen vornehmen:
- Root-Passwort setzen
- Anonyme Benutzer entfernen
- Root-Login von extern nicht erlauben
- Testdatenbank entfernen
- Rechte neu laden

Passe anschließend die Konfiguration an:
```bash
sudo nano /etc/mysql/my.cnf
```
Füge folgende Zeilen hinzu:
```
[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

[mysql]
default-character-set = utf8mb4
```
Starte den Datenbankserver neu:
```bash
sudo service mysql restart
```

## 4. Frappe Bench installieren
Installiere das Frappe-Bench-Tool zur Verwaltung der Frappe-Anwendungen:
```bash
sudo -H pip3 install frappe-bench --break-system-packages
sudo -H pip3 install ansible --break-system-packages
bench init frappe-bench --frappe-branch version-15
cd frappe-bench
chmod -R o+rx /home/[frappe-user]
```

## 5. ERPNext installieren
### Neue Site erstellen
Richte eine neue ERPNext-Site ein:
```bash
bench new-site [your-site-name]
```

### ERPNext und Abhängigkeiten herunterladen
Lade die ERPNext-App aus dem offiziellen Repository:
```bash
bench get-app --branch version-15 payments
bench get-app --branch version-15 erpnext
```

### ERPNext und Payments installieren

Die Payments-App ist eine Voraussetzung für ERPNext, da sie grundlegende Zahlungsfunktionen bereitstellt. Deshalb muss sie vor ERPNext installiert werden.
Die Payments-App ist eine Voraussetzung für ERPNext und sollte vor der Installation von ERPNext installiert werden.
Installiere die App auf der erstellten Site:
```bash
bench --site [your-site-name] install-app payments
bench --site [your-site-name] install-app erpnext
```

## 6. Spherdex installieren
### Spherdex App herunterladen
Spherdex wird als eigenständige App in Frappe installiert:
```bash
bench get-app --branch version-15 spherdex
```

### Spherdex App installieren
Installiere Spherdex auf der erstellten Site:
```bash
bench --site [your-site-name] install-app spherdex
```

## 7. Einrichtung & Konfiguration
### Supervisor einrichten
Supervisor wird verwendet, um Hintergrundprozesse zu verwalten:
```bash
bench setup supervisor
sudo ln -s $(pwd)/config/supervisor.conf /etc/supervisor/conf.d/frappe.conf
sudo supervisorctl reread && sudo supervisorctl update && sudo supervisorctl restart all
```

### Nginx Konfiguration
Setze den Webserver für die Anwendung auf:
```bash
bench setup nginx
sudo ln -s $(pwd)/config/nginx.conf /etc/nginx/sites-enabled/frappe
sudo systemctl restart nginx
```

## 8. Abschluss & Überprüfung
Starte den Bench-Server:
```bash
bench start
```
Überprüfe, ob die Anwendung erreichbar ist:
```bash
curl -I http://[your-server-ip]
```

## 9. Troubleshooting
Falls Probleme auftreten, können folgende Befehle zur Diagnose helfen:
```bash
bench doctor
bench restart
sudo supervisorctl status
```

## 10. Produktivbetrieb

Der Produktivmodus sorgt dafür, dass ERPNext und Spherdex dauerhaft als systemweite Dienste laufen. Dies bedeutet, dass die Anwendungen nicht jedes Mal manuell mit `bench start` gestartet werden müssen. Der Produktivmodus ist besonders wichtig für eine stabile und zuverlässige Nutzung, da er:

- Automatische Neustarts nach einem Server-Neustart ermöglicht
- Die Performance optimiert
- Prozesse über **Supervisor** verwaltet
- **Nginx** als stabilen Webserver einsetzt

Ohne den Produktivmodus wäre es notwendig, die Anwendung manuell zu starten, was für einen produktiven Einsatz nicht praktikabel ist.

Der Produktivmodus sorgt dafür, dass ERPNext und Spherdex als systemweite Dienste laufen, anstatt manuell mit `bench start` gestartet zu werden. Dadurch wird sichergestellt, dass die Anwendung auch nach einem Neustart des Servers automatisch verfügbar ist. Außerdem verbessert der Produktivmodus die Performance und Stabilität der Umgebung, indem Prozesse über **Supervisor** verwaltet und über **Nginx** als Webserver bereitgestellt werden.
### Scheduler aktivieren
Scheduler für geplante Aufgaben aktivieren:
```bash
bench --site [your-site-name] enable-scheduler
```

### Wartungsmodus deaktivieren
Sicherstellen, dass das System aktiv bleibt:
```bash
bench --site [your-site-name] set-maintenance-mode off
```

### Produktion aktivieren
Die Aktivierung des Produktivmodus konfiguriert das System so, dass ERPNext und Spherdex als Hintergrunddienste betrieben werden. Dies bedeutet:
- Automatischer Start der Anwendung nach einem Server-Neustart
- Nutzung von Supervisor zur Verwaltung der Prozesse
- Verwendung von Nginx als Reverse Proxy für bessere Performance
- Sicherheitseinstellungen für den stabilen Betrieb
Aktiviere den Produktivmodus für Bench:
```bash
sudo bench setup production [frappe-user]
```

### Nginx Konfiguration anwenden
Stelle sicher, dass Nginx die neuen Einstellungen übernimmt:
```bash
bench setup nginx
```

### Supervisor neu starten
Alle Dienste für den Produktivbetrieb neu starten:
```bash
sudo supervisorctl restart all
sudo bench setup production [frappe-user]
```

### Sicherheit verbessern
- **HTTPS aktivieren** mit Let’s Encrypt:
  ```bash
  sudo bench setup lets-encrypt [your-site-name]
  ```
- **Firewall konfigurieren**:
  ```bash
  sudo ufw allow OpenSSH
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp
  sudo ufw enable
  ```

---

Damit ist die Installation und der Produktivbetrieb von **Spherdex** abgeschlossen. 🎯

