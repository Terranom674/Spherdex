frappe.ui.form.on('Admin Einstellungen', {
    refresh: function(frm) {
        // Überprüfen, ob die Sperre aktiv ist und das Kontrollkästchen sperren, wenn der Benutzer nicht der aktive User ist
        if (frm.doc.datenbank_gesperrt && frm.doc.active_user !== frappe.session.user) {
            frm.set_df_property('datenbank_gesperrt', 'read_only', 1);
        } else {
            frm.set_df_property('datenbank_gesperrt', 'read_only', 0);
        }
    },

    datenbank_gesperrt: function(frm) {
        console.log("Checkbox geändert.");  // Debug-Log

        frappe.call({
            method: 'spherdex.global_scripts.utils.set_database_lock',
            args: { status: frm.doc.datenbank_gesperrt ? "sperren" : "entsperren", user: frappe.session.user },
            callback: function(response) {
                frappe.msgprint(response.message);

                // Direkt den Wert speichern, ohne manuelles Speichern
                frappe.model.set_value(frm.doctype, frm.docname, 'datenbank_gesperrt', frm.doc.datenbank_gesperrt);
                frm.reload_doc(); // Formular nach Änderung neu laden, um den aktuellen Status zu reflektieren
            }
        });
    }
});
