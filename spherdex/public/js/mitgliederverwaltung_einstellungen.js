frappe.ui.form.on('Mitgliederverwaltung Einstellungen', {
    standardrollen_button: function(frm) {
        frappe.call({
            method: "path.to.your.module.standard_roles.install_standard_roles",
            callback: function(r) {
                if (r.message) {
                    frappe.msgprint(r.message);
                }
            }
        });
    }
});