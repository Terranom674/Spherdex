frappe.ui.form.on('Mitglied', {
    refresh: function (frm) {
        // Abrufen der Einstellung für den Anzeigemodus
        frappe.call({
            method: 'spherdex.global_scripts.utils.get_settings',
            callback: function (r) {
                if (r.message) {
                    const anzeigenmodus = r.message.default_anzeigenmodus;

                    // Rollen abrufen und Felder initialisieren
                    frappe.call({
                        method: 'spherdex.global_scripts.utils.fetch_roles',
                        callback: function (res) {
                            if (res.message && Array.isArray(res.message)) {
                                const rollen = res.message;

                                // Aktuelle Werte aus rollen_werte laden
                                const selectedRoles = frm.doc.rollen_werte
                                    ? frm.doc.rollen_werte.split(', ').map(role => role.trim())
                                    : [];

                                // Checkboxen initialisieren
                                const checkboxContainer = $(frm.fields_dict.rollen_checkboxes.wrapper).empty();
                                let checkboxHtml = '<div class="roles-container">';
                                rollen.forEach(role => {
                                    const isChecked = selectedRoles.includes(role.rollenname) ? 'checked' : '';
                                    checkboxHtml += `
                                        <div>
                                            <input type="checkbox" id="${role.name}" name="rollen" value="${role.rollenname}" ${isChecked}>
                                            <label for="${role.name}">${role.rollenname}</label>
                                        </div>
                                    `;
                                });
                                checkboxHtml += '</div>';
                                checkboxContainer.html(checkboxHtml);

                                // MultiSelect initialisieren
                                const multiSelectContainer = $(frm.fields_dict.rollen_multiselect.wrapper).empty();
                                let multiSelectHtml = '<select multiple="multiple" style="width:100%;">';
                                rollen.forEach(role => {
                                    const isSelected = selectedRoles.includes(role.rollenname) ? 'selected' : '';
                                    multiSelectHtml += `<option value="${role.rollenname}" ${isSelected}>${role.rollenname}</option>`;
                                });
                                multiSelectHtml += '</select>';
                                multiSelectContainer.html(multiSelectHtml);

                                // Sichtbarkeit basierend auf der Einstellung steuern
                                if (anzeigenmodus === 'Checkbox') {
                                    frm.fields_dict.rollen_checkboxes.df.hidden = 0;
                                    frm.fields_dict.rollen_multiselect.df.hidden = 1;
                                } else if (anzeigenmodus === 'MultiSelect') {
                                    frm.fields_dict.rollen_checkboxes.df.hidden = 1;
                                    frm.fields_dict.rollen_multiselect.df.hidden = 0;
                                }

                                frm.refresh_field('rollen_checkboxes');
                                frm.refresh_field('rollen_multiselect');

                                // Synchronisierung der Auswahl
                                setupSynchronization(frm);
                            } else {
                                console.error("Keine Rollen verfügbar oder API-Fehler:", res.message);
                            }
                        }
                    });
                } else {
                    console.error("Fehler beim Abrufen der Einstellungen:", r.message);
                }
            }
        });
    },
    before_save: function (frm) {
        // Rollen aus dem aktiven Feld in rollen_werte synchronisieren
        let selectedRoles = [];
        if (frm.fields_dict.rollen_checkboxes.df.hidden === 0) {
            // Checkbox-Feld ist sichtbar
            $(frm.fields_dict.rollen_checkboxes.wrapper)
                .find('input[type="checkbox"]:checked')
                .each(function () {
                    selectedRoles.push($(this).val());
                });
        } else if (frm.fields_dict.rollen_multiselect.df.hidden === 0) {
            // MultiSelect-Feld ist sichtbar
            selectedRoles = $(frm.fields_dict.rollen_multiselect.wrapper).find('select').val() || [];
        }

        // Setze die Werte in das Hidden Field
        frm.set_value('rollen_werte', selectedRoles.join(', '));
    }
});

function setupSynchronization(frm) {
    // Synchronisierung von Checkbox -> MultiSelect
    $(frm.fields_dict.rollen_checkboxes.wrapper).on('change', 'input[type="checkbox"]', function () {
        const selectedValues = [];
        $(frm.fields_dict.rollen_checkboxes.wrapper)
            .find('input[type="checkbox"]:checked')
            .each(function () {
                selectedValues.push($(this).val());
            });

        // Setze Auswahl im MultiSelect
        const multiSelect = $(frm.fields_dict.rollen_multiselect.wrapper).find('select');
        multiSelect.val(selectedValues).trigger('change');
    });

    // Synchronisierung von MultiSelect -> Checkbox
    $(frm.fields_dict.rollen_multiselect.wrapper).on('change', 'select', function () {
        const selectedValues = $(this).val() || [];
        $(frm.fields_dict.rollen_checkboxes.wrapper)
            .find('input[type="checkbox"]')
            .each(function () {
                const isChecked = selectedValues.includes($(this).val());
                $(this).prop('checked', isChecked);
            });
    });
}
