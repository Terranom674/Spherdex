frappe.ui.form.on("Mitgliederverwaltung Einstellungen", {
    refresh: function (frm) {
        console.log("Formular 'Mitgliederverwaltung Einstellungen' wurde geladen.");

        // Button "Standardrollen installieren"
        frm.fields_dict.standardrollen_button.$wrapper.find('button').on('click', function () {
            console.log("Button 'Standardrollen installieren' wurde geklickt!");
            frappe.call({
                method: "spherdex.global_scripts.member_management.install_standard_roles",
                callback: function (response) {
                    frappe.msgprint("Standardrollen wurden erfolgreich installiert!");
                    frm.reload_doc(); // Neu laden
                }
            });
        });

        // Button "Präfix ändern"
        frm.fields_dict.prefix_aendern.$wrapper.find('button').on('click', function () {
            console.log("Button 'Präfix ändern' wurde geklickt!");
            frappe.prompt(
                [{ label: 'Neues Präfix', fieldname: 'new_prefix', fieldtype: 'Data', reqd: 1 }],
                function (values) {
                    frappe.call({
                        method: "spherdex.global_scripts.member_management.update_prefix",
                        args: { new_prefix: values.new_prefix },
                        callback: function (response) {
                            frappe.msgprint("Präfix wurde erfolgreich geändert!");
                            frm.reload_doc(); // Neu laden
                        }
                    });
                },
                'Präfix ändern',
                'Bestätigen'
            );
        });

        // Button "Neu durchnummerieren"
        frm.fields_dict.neu_durchzaehlen.$wrapper.find('button').on('click', function () {
            console.log("Button 'Neu durchnummerieren' wurde geklickt!");
            frappe.confirm(
                'Möchten Sie alle Mitglieder neu durchnummerieren?',
                function () {
                    frappe.call({
                        method: "spherdex.global_scripts.member_management.renumber_members",
                        callback: function (response) {
                            frappe.msgprint("Alle Mitglieder wurden erfolgreich neu durchnummeriert!");
                            frm.reload_doc(); // Neu laden
                        }
                    });
                }
            );
        });

        // Button "Präfix und Nummer aktualisieren"
        frm.fields_dict.prefix_und_nummer.$wrapper.find('button').on('click', function () {
            console.log("Button 'Präfix und Nummer aktualisieren' wurde geklickt!");
            frappe.prompt(
                [{ label: 'Neues Präfix', fieldname: 'new_prefix', fieldtype: 'Data', reqd: 1 }],
                function (values) {
                    frappe.call({
                        method: "spherdex.global_scripts.member_management.update_prefix_and_number",
                        args: { new_prefix: values.new_prefix },
                        callback: function (response) {
                            frappe.msgprint("Präfix und Nummer wurden erfolgreich aktualisiert!");
                            frm.reload_doc(); // Neu laden
                        }
                    });
                },
                'Präfix und Nummer aktualisieren',
                'Bestätigen'
            );
        });

        // Button "Alle Mitglieder löschen"
        frm.fields_dict.alle_mitglieder_loeschen.$wrapper.find('button').on('click', function () {
            console.log("Button 'Alle Mitglieder löschen' wurde geklickt!");
            frappe.confirm(
                'Möchten Sie wirklich alle Mitglieder löschen? Diese Aktion kann nicht rückgängig gemacht werden.',
                function () {
                    frappe.call({
                        method: "spherdex.global_scripts.member_management.delete_all_members",
                        callback: function (response) {
                            frappe.msgprint("Alle Mitglieder wurden erfolgreich gelöscht!");
                            frm.reload_doc(); // Neu laden
                        }
                    });
                }
            );
        });

        // Button "Neues Format anwenden"
        frm.fields_dict.neues_format.$wrapper.find('button').on('click', function () {
            console.log("Button 'Neues Format anwenden' wurde geklickt!");
            frappe.prompt(
                [{ label: 'Neues Format', fieldname: 'new_format', fieldtype: 'Data', reqd: 1 }],
                function (values) {
                    frappe.call({
                        method: "spherdex.global_scripts.member_management.apply_new_format",
                        args: { new_format: values.new_format },
                        callback: function (response) {
                            frappe.msgprint("Neues Format wurde erfolgreich angewendet!");
                            frm.reload_doc(); // Neu laden
                        }
                    });
                },
                'Neues Format anwenden',
                'Bestätigen'
            );
        });
    }
});
