frappe.provide('custom.onload_handlers');

custom.onload_handlers.member_import = function(listview) {
    console.log("✅ member_import.js wurde geladen!");
    console.log("👉 listview Objekt:", listview);

    if (!listview || !listview.page) {
        console.warn("⚠️ listview oder listview.page ist undefined! Der Import-Button kann nicht hinzugefügt werden.");
        return;
    }

    console.log("✅ Füge Import-Button zur Action Bar hinzu...");

    listview.page.add_inner_button(__('📥 CSV Importieren'), function() {
        let dialog = new frappe.ui.Dialog({
            title: 'CSV-Mitgliederimport',
            fields: [
                { fieldname: 'file', fieldtype: 'Attach', label: 'CSV-Datei hochladen' }
            ],
            primary_action_label: 'Import starten',
            primary_action(values) {
                if (!values.file) {
                    frappe.msgprint("❌ Bitte eine CSV-Datei hochladen!");
                    return;
                }

                console.log("📥 Datei-Upload erkannt:", values.file);

                // **Datei-URL bereinigen (Frappe speichert manchmal `/private/files/` davor)**
                let file_url = values.file;
                if (!file_url.startsWith("/files/") && !file_url.startsWith("/private/files/")) {
                    file_url = "/files/" + file_url;
                }

                console.log("📁 Bereinigte Datei-URL:", file_url);

                // **Prüfen, ob die Datei wirklich existiert**
                frappe.call({
                    method: "frappe.client.get",
                    args: {
                        doctype: "File",
                        filters: { file_url: file_url }
                    },
                    callback: function(response) {
                        if (response.message) {
                            console.log("✅ Datei existiert in der Datenbank:", response.message);

                            // **Jetzt erst den Import starten**
                            frappe.call({
                                method: "spherdex.api.member_import.upload_csv",
                                args: { file_url: file_url },
                                callback: function(r) {
                                    if (r.message.status === "success") {
                                        frappe.msgprint({
                                            title: __('Import Erfolgreich'),
                                            message: r.message.message,
                                            indicator: 'green'
                                        });

                                        listview.refresh();
                                    } else {
                                        frappe.msgprint({
                                            title: __('Fehler beim Import'),
                                            message: r.message.message || "Ein Fehler ist aufgetreten.",
                                            indicator: 'red'
                                        });
                                        console.error(r.message.errors);
                                    }
                                }
                            });

                            dialog.hide();
                        } else {
                            frappe.msgprint("⚠️ Datei wurde noch nicht gespeichert. Bitte erneut versuchen.");
                            console.warn("❌ Datei wurde nicht in der Datenbank gefunden.");
                        }
                    }
                });
            }
        });

        dialog.show();
    });

    console.log("✅ Import-Button erfolgreich hinzugefügt!");
};
