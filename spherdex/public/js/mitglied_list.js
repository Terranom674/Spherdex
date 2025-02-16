frappe.provide('custom.onload_handlers');

custom.onload_handlers.mitglied_list = function(listview) {
    console.log("Mitglied ListView geladen");

    let downloadButton;
    let lastFileUrl = null;

    // 📌 **Download-Button hinzufügen (erst sichtbar machen, wenn Datei vorhanden ist)**
    function addDownloadButton(file_url) {
        lastFileUrl = file_url;
        if (!downloadButton) {
            downloadButton = listview.page.add_inner_button(__('📥 Datei herunterladen'), function() {
                triggerDownload(lastFileUrl);
            });
            downloadButton.hide();
        }
        downloadButton.show();
    }

    // 📌 **Erzwingt "Speichern unter"-Dialog & löscht Datei nach dem Speichern**
    function triggerDownload(url) {
        let a = document.createElement("a");
        a.href = url;
        a.download = url.split('/').pop();  // Erzwingt "Speichern unter"
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        console.log("📥 Datei wurde gespeichert – Löschung beginnt...");

        // 🔥 Datei jetzt endgültig vom Server löschen
        frappe.call({
            method: "spherdex.api.export_mitglieder.delete_export_files",
            callback: function(r) {
                console.log("🗑 Datei gelöscht nach Speicherung:", r.message);
                if (downloadButton) {
                    downloadButton.hide();
                }
            },
            error: function(err) {
                console.error("❌ Fehler beim Löschen:", err);
            }
        });
    }

    // 📌 **Export-Button mit allen Formaten**
    listview.page.add_inner_button(__('📤 Export starten'), function() {
        let dialog = new frappe.ui.Dialog({
            title: 'Mitglieder-Export',
            fields: [
                { fieldname: 'fields', fieldtype: 'MultiCheck', label: 'Felder auswählen', 
                  options: [
                      { label: 'Vorname', value: 'vorname', checked: 1 },
                      { label: 'Nachname', value: 'nachname', checked: 1 },
                      { label: 'Mitgliedsnummer', value: 'name', checked: 1 },
                      { label: 'Status', value: 'status', checked: 1 },
                      { label: 'E-Mail', value: 'mail_privat' },
                      { label: 'Telefon', value: 'handy' },
                      { label: 'Adresse', value: 'adresse' },
                      { label: 'Eintrittsdatum', value: 'eintrittsdatum' }
                  ] 
                },
                { fieldname: 'only_active', fieldtype: 'Check', label: 'Nur aktive Mitglieder' },
                { fieldname: 'file_format', fieldtype: 'Select', label: 'Exportformat', 
                  options: ['csv', 'xlsx', 'docx', 'pdf', 'txt'], default: 'csv' }
            ],
            primary_action_label: 'Export starten',
            primary_action(values) {
                console.log("📤 Export wird gestartet mit Werten:", values);

                frappe.call({
                    method: "spherdex.api.export_mitglieder.export_data_async",
                    args: values,
                    callback: function(r) {
                        if (r.message.status === "Export gestartet") {
                            frappe.msgprint("Export wurde gestartet. Sie erhalten eine Benachrichtigung, sobald die Datei fertig ist.");
                        } else {
                            frappe.msgprint({
                                title: "Fehler",
                                message: r.message.message,
                                indicator: "red"
                            });
                        }
                    },
                    error: function(err) {
                        console.error("❌ Fehler beim Aufruf:", err);
                    }
                });

                dialog.hide();
            }
        });

        dialog.show();
    });

    // 📌 **Echtzeit-Event `export_complete` überwachen**
    frappe.realtime.on("export_complete", (data) => {
        console.log("🔔 Echtzeit-Event erhalten:", data);
        if (data.status === "success") {
            let file_url = data.file_url;

            // 📌 **Download-Button aktivieren**
            addDownloadButton(file_url);

            // 📌 **Benachrichtigung mit klickbarem Download-Link**
            frappe.show_alert({
                message: `📥 <b>Export abgeschlossen!</b> <br>
                    <a href="${file_url}" target="_blank" id="exportDownloadLink" style="color: blue; font-weight: bold;">👉 Datei herunterladen</a>`,
                indicator: 'green'
            }, 10);

            // 📌 **Löschung auch über Klick auf Link ausführen**
            setTimeout(() => {
                let downloadLink = document.getElementById("exportDownloadLink");
                if (downloadLink) {
                    downloadLink.addEventListener("click", function(event) {
                        event.preventDefault();  // Direktes Öffnen verhindern
                        triggerDownload(file_url);
                    });
                }
            }, 1000);
        } else {
            frappe.show_alert({
                message: `❌ Fehler beim Export: ${data.message}`,
                indicator: 'red'
            }, 10);
        }
    });
};
