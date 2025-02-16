frappe.ui.form.on('Admin Einstellungen', {
    refresh: function(frm) {
        // Überprüfen, ob die Sperre aktiv ist und das Kontrollkästchen sperren, wenn der Benutzer nicht der aktive User ist
        if (frm.doc.datenbank_gesperrt && frm.doc.active_user !== frappe.session.user) {
            frm.set_df_property('datenbank_gesperrt', 'read_only', 1);
        } else {
            frm.set_df_property('datenbank_gesperrt', 'read_only', 0);
        }

        if (!frm.custom_buttons_added) {
            addCustomButtons(frm, 'top');    // Buttons oben
            addCustomButtons(frm, 'bottom'); // Buttons unten
            frm.custom_buttons_added = true;
        }

        loadProtokoll(frm, 5, 1); // Standardmäßig 5 Einträge auf Seite 1 laden

        frm.ignore_doctype_change = true;  // 🔥 Verhindert, dass UI-Änderungen als Änderungen im Doctype erkannt werden
        frm.disable_save();  // 🔥 Verhindert, dass das Speichern-Icon erscheint
    },

    datenbank_gesperrt: function(frm) {
        console.log("Checkbox geändert.");  // Debug-Log

        frappe.call({
            method: 'spherdex.utils.utils.set_database_lock',  // ✅ Korrigierter Pfad
            args: { status: frm.doc.datenbank_gesperrt ? "sperren" : "entsperren", user: frappe.session.user },
            callback: function(response) {
                frappe.msgprint(response.message);
                frappe.model.set_value(frm.doctype, frm.docname, 'datenbank_gesperrt', frm.doc.datenbank_gesperrt);
                frm.reload_doc();
            }
        });
    }
});

function addCustomButtons(frm, position) {
    if ($(`.button-container-${position}`).length) {
        return;
    }

    const limits = [5, 10, 100, 'Alle'];
    const container = $(`<div class="button-container-${position}" style="text-align: right; margin: 10px 0;"></div>`);

    if (position === 'top') {
        frm.fields_dict.sperr_protokoll.grid.wrapper.before(container);
    } else {
        frm.fields_dict.sperr_protokoll.grid.wrapper.after(container);
    }

    limits.forEach(limit => {
        const button = $(`<button class="btn btn-sm btn-primary" style="margin: 2px;">${limit}</button>`);
        button.on('click', () => loadProtokoll(frm, limit, 1));
        container.append(button);
    });

    const deleteButton = $(`<button class="btn btn-sm btn-danger" style="margin: 2px;">Löschen</button>`);
    deleteButton.on('click', () => {
        frappe.confirm('Alle Protokolleinträge wirklich löschen?', () => {
            frappe.call({
                method: 'spherdex.utils.utils.clear_protokoll',
                callback: function() {
                    frappe.msgprint('Alle Einträge gelöscht.');
                    loadProtokoll(frm, 5, 1);
                }
            });
        });
    });
    container.append(deleteButton);
}

function loadProtokoll(frm, limit, page) {
    frappe.call({
        method: 'spherdex.utils.utils.get_protokoll',
        args: { limit: limit, page: page },
        callback: function(response) {
            const entries = response.message.data || [];
            const total_pages = response.message.total_pages;
            const current_page = response.message.current_page;

            frappe.run_serially([
                () => frm.clear_table("sperr_protokoll"),
                () => {
                    entries.forEach(entry => {
                        let row = frm.add_child("sperr_protokoll");
                        row.zeitpunkt = entry.zeitpunkt;
                        row.aktion = entry.aktion;
                        row.benutzer = entry.benutzer;
                        row.sperrgrund = entry.sperrgrund;
                    });
                },
                () => frm.refresh_field("sperr_protokoll"),
                () => addPaginationControls(frm, limit, current_page, total_pages)
            ]);
        }
    });
}

function addPaginationControls(frm, limit, current_page, total_pages) {
    $('.pagination-controls').remove();

    if (total_pages <= 1) return;

    const paginationContainer = $('<div class="pagination-controls" style="text-align: center; margin: 10px 0;"></div>');

    if (current_page > 1) {
        const prevButton = $(`<button class="btn btn-outline-secondary btn-sm" style="margin: 2px;">« Vorherige</button>`);
        prevButton.on('click', () => loadProtokoll(frm, limit, current_page - 1));
        paginationContainer.append(prevButton);
    }

    for (let i = 1; i <= total_pages; i++) {
        const button = $(`<button class="btn btn-outline-secondary btn-sm" style="margin: 2px;">${i}</button>`);
        if (i === current_page) button.addClass("btn-primary");
        button.on('click', () => loadProtokoll(frm, limit, i));
        paginationContainer.append(button);
    }

    if (current_page < total_pages) {
        const nextButton = $(`<button class="btn btn-outline-secondary btn-sm" style="margin: 2px;">Nächste »</button>`);
        nextButton.on('click', () => loadProtokoll(frm, limit, current_page + 1));
        paginationContainer.append(nextButton);
    }

    frm.fields_dict.sperr_protokoll.grid.wrapper.after(paginationContainer);
}
