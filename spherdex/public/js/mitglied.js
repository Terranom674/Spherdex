frappe.ui.form.on('Mitglied', {
    refresh: function (frm) {
        if (!frm.is_new()) {
            // 📥 Export-Button für Einzelmitglied
            frm.add_custom_button(__('📥 Mitgliedsakte exportieren'), function() {
                frappe.prompt([
                    {
                        fieldname: "format",
                        label: "Exportformat",
                        fieldtype: "Select",
                        options: ["PDF", "CSV", "DOCX", "XLSX", "TXT"],
                        default: "PDF"
                    }
                ], function(values) {
                    frappe.call({
                        method: "spherdex.global_scripts.export_utils.export_data_async",
                        args: {
                            member_id: frm.doc.name,  // ✅ Falls gesetzt, wird nur dieses Mitglied exportiert
                            file_format: values.format.toLowerCase()
                        },
                        callback: function(r) {
                            if (r.message.status === "Export gestartet") {
                                frappe.show_alert({
                                    message: "Export wurde gestartet. Sie erhalten eine Benachrichtigung, sobald die Datei fertig ist.",
                                    indicator: "blue"
                                });
                            } else {
                                frappe.msgprint("Fehler beim Export.");
                            }
                        }
                    });
                }, __("Exportoptionen"), __("Export starten"));
            }).addClass("btn-primary");
        }

        // 🔔 Echtzeit-Event für Export-Abschluss
        frappe.realtime.on("export_complete", (data) => {
            console.log("🔔 Export abgeschlossen:", data);
            if (data.status === "success") {
                let file_url = data.file_url;

                // 🆕 Download-Button nach Export einfügen
                if (!frm.fields_dict.export_download_section) {
                    frm.add_custom_button(__('📥 Datei herunterladen'), function() {
                        window.open(file_url, "_blank");
                    }).addClass("btn-success");
                }

                // 📥 Benachrichtigung mit Download-Link
                frappe.show_alert({
                    message: `📥 <b>Export abgeschlossen!</b> <br>
                        <a href="${file_url}" target="_blank" id="exportDownloadLink"
                           style="color: blue; font-weight: bold;">👉 Datei herunterladen</a>`,
                    indicator: 'green'
                }, 10);

                // 🗑 Datei wird erst nach erfolgreichem Download gelöscht
                setTimeout(() => {
                    document.getElementById("exportDownloadLink").addEventListener("click", function() {
                        setTimeout(() => {
                            frappe.call({
                                method: "spherdex.global_scripts.export_utils.delete_export_files",
                                callback: function(r) {
                                    console.log("🗑 Dateien gelöscht:", r.message);
                                }
                            });
                        }, 5000);
                    });
                }, 1000);
            } else {
                frappe.show_alert({
                    message: `❌ Fehler beim Export: ${data.message}`,
                    indicator: 'red'
                }, 10);
            }
        });

        // 🔄 Bestehende UI-Initialisierung beibehalten
        setupMemberUI(frm);
    },
    before_save: function (frm) {
        syncRoles(frm);
    }
});

// 🔄 Bestehende UI- & Rollen-Funktionen
function setupMemberUI(frm) {
    frappe.call({
        method: 'spherdex.global_scripts.utils.get_settings',
        callback: function (r) {
            if (r.message) {
                const anzeigenmodus = r.message.default_anzeigenmodus;
                loadRoles(frm, anzeigenmodus);
            }
        }
    });
}

function loadRoles(frm, anzeigenmodus) {
    frappe.call({
        method: 'spherdex.global_scripts.utils.fetch_roles',
        callback: function (res) {
            if (res.message && Array.isArray(res.message)) {
                setupRoleFields(frm, res.message, anzeigenmodus);
            }
        }
    });
}

function setupRoleFields(frm, rollen, anzeigenmodus) {
    const selectedRoles = frm.doc.rollen_werte
        ? frm.doc.rollen_werte.split(', ').map(role => role.trim())
        : [];

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

    const multiSelectContainer = $(frm.fields_dict.rollen_multiselect.wrapper).empty();
    let multiSelectHtml = '<select multiple="multiple" style="width:100%;">';
    rollen.forEach(role => {
        const isSelected = selectedRoles.includes(role.rollenname) ? 'selected' : '';
        multiSelectHtml += `<option value="${role.rollenname}" ${isSelected}>${role.rollenname}</option>`;
    });
    multiSelectHtml += '</select>';
    multiSelectContainer.html(multiSelectHtml);

    frm.fields_dict.rollen_checkboxes.df.hidden = (anzeigenmodus !== 'Checkbox') ? 1 : 0;
    frm.fields_dict.rollen_multiselect.df.hidden = (anzeigenmodus !== 'MultiSelect') ? 1 : 0;

    frm.refresh_field('rollen_checkboxes');
    frm.refresh_field('rollen_multiselect');

    setupSynchronization(frm);
}

function syncRoles(frm) {
    let selectedRoles = [];
    if (frm.fields_dict.rollen_checkboxes.df.hidden === 0) {
        $(frm.fields_dict.rollen_checkboxes.wrapper)
            .find('input[type="checkbox"]:checked')
            .each(function () {
                selectedRoles.push($(this).val());
            });
    } else if (frm.fields_dict.rollen_multiselect.df.hidden === 0) {
        selectedRoles = $(frm.fields_dict.rollen_multiselect.wrapper).find('select').val() || [];
    }
    frm.set_value('rollen_werte', selectedRoles.join(', '));
}

function setupSynchronization(frm) {
    $(frm.fields_dict.rollen_checkboxes.wrapper).on('change', 'input[type="checkbox"]', function () {
        const selectedValues = [];
        $(frm.fields_dict.rollen_checkboxes.wrapper)
            .find('input[type="checkbox"]:checked')
            .each(function () {
                selectedValues.push($(this).val());
            });

        $(frm.fields_dict.rollen_multiselect.wrapper).find('select').val(selectedValues).trigger('change');
    });

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
