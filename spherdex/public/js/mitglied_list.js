frappe.listview_settings['Mitglied'] = {
    onload: function(listview) {
        let downloadButton;

        // 📌 **Download-Button hinzufügen (aber versteckt)**
        function addDownloadButton(file_url) {
            if (!downloadButton) {
                downloadButton = listview.page.add_inner_button(__('📥 CSV herunterladen'), function() {
                    window.open(file_url, "_blank");
                });
                downloadButton.hide();
            }
        }

        // 📌 **Prüft `export_ready` in `frappe.cache()`**
        function checkExportReady() {
            frappe.call({
                method: "frappe.utils.redis_wrapper.get_value",
                args: { key: "export_ready" },
                callback: function(r) {
                    console.log("🔍 Status von export_ready:", r.message);
                    if (r.message === "true") {
                        console.log("✅ Export ist bereit, Button anzeigen!");
                        if (downloadButton) {
                            downloadButton.show();
                        }
                    } else {
                        console.log("❌ Export noch nicht bereit.");
                        if (downloadButton) {
                            downloadButton.hide();
                        }
                    }
                }
            });
        }

        // 📌 **Export-Button für den Start**
        listview.page.add_inner_button(__('CSV Export'), function() {
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
                    { fieldname: 'since_date', fieldtype: 'Date', label: 'Eintrittsdatum ab' }
                ],
                primary_action_label: 'Export starten',
                primary_action(values) {
                    console.log("📤 Sende Export-Request mit:", values);

                    frappe.call({
                        method: "spherdex.mitgliederverwaltung.doctype.mitglied.mitglied.export_members_csv_async",
                        args: values,
                        callback: function(r) {
                            console.log("📩 Antwort erhalten:", r);
                            if (r.message.status === "Export gestartet") {
                                frappe.msgprint("Export wurde gestartet. Sie erhalten eine Benachrichtigung, sobald die Datei fertig ist.");
                                
                                // 🔄 **Regelmäßig prüfen, ob Export bereit ist**
                                let checkInterval = setInterval(function() {
                                    checkExportReady();
                                    if (downloadButton && downloadButton.is(":visible")) {
                                        clearInterval(checkInterval);
                                    }
                                }, 5000);
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
                        <a href="${file_url}" target="_blank" style="color: blue; font-weight: bold;">👉 Datei herunterladen</a>`,
                    indicator: 'green'
                }, 10);

            } else {
                frappe.show_alert({
                    message: `❌ Fehler beim Export: ${data.message}`,
                    indicator: 'red'
                }, 10);
            }
        });
    } 
};