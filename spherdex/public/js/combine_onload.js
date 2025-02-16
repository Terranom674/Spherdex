frappe.provide('custom.onload_handlers');

frappe.listview_settings['Mitglied'] = frappe.listview_settings['Mitglied'] || {};

let existing_onload = frappe.listview_settings['Mitglied'].onload;

frappe.listview_settings['Mitglied'].onload = function(listview) {
    if (existing_onload) {
        existing_onload(listview);
    }

    if (custom.onload_handlers.mitglied_list) {
        custom.onload_handlers.mitglied_list(listview);
    }

    if (custom.onload_handlers.member_import) {
        custom.onload_handlers.member_import(listview);
    }
};
