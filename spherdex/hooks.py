app_name = "spherdex"
app_title = "Spherdex"
app_publisher = "Thomas Dannenberg"
app_description = "App zur Verwaltung von Mitgliedern, Veranstaltungen, Inventar und vielem mehr. Die Komplettlösung für jeden Verein, Club oder Verbund."
app_email = "thomas_dannenberg@web.de"
app_license = "agpl-3.0"

# Includes in <head>
# ------------------
# include js, css files in header of desk.html
# app_include_css = "/assets/spherdex/css/spherdex.css"
# app_include_js = "/assets/spherdex/js/spherdex.js"

app_include_js = [
    "/assets/spherdex/js/combine_onload.js",
    "/assets/spherdex/js/mitglied_list.js",
    "/assets/spherdex/js/member_import.js",
    "/assets/spherdex/js/custom_menu.js"
]



# include js, css files in header of web template
# web_include_css = "/assets/spherdex/css/spherdex.css"
# web_include_js = "/assets/spherdex/js/spherdex.js"

# include js in doctype views
doctype_js = {
    "Mitgliederverwaltung Einstellungen": "public/js/mitgliederverwaltung_einstellungen.js",
    "Mitglied": "public/js/mitglied.js",
    "Admin Einstellungen": "public/js/admin_einstellungen.js"
}

# Document Events
# ---------------
doc_events = {
    "*": {  # Gilt für alle Doctypes
        "before_save": "spherdex.utils.utils.validate_database_lock",
        "before_submit": "spherdex.utils.utils.validate_database_lock",
        "before_cancel": "spherdex.utils.utils.validate_database_lock",
        "before_delete": "spherdex.utils.utils.validate_database_lock"
    }
}

# Scheduled Tasks
# ---------------
# scheduler_events = {
#     "daily": [
#         "spherdex.utils.member_management.daily_tasks"
#     ]
# }

# Jinja
# ----------
# add methods and filters to jinja environment
# jinja = {
#     "methods": "spherdex.utils.jinja_methods",
#     "filters": "spherdex.utils.jinja_filters"
# }

# Permissions
# -----------
# permission_query_conditions = {
#     "Mitglied": "spherdex.utils.member_management.get_permission_query_conditions",
# }
# has_permission = {
#     "Mitglied": "spherdex.utils.member_management.has_permission",
# }

# Installation
# ------------
# before_install = "spherdex.install.before_install"
# after_install = "spherdex.install.after_install"

after_install = "spherdex.config.install.after_install"

# Uninstallation
# --------------
# before_uninstall = "spherdex.uninstall.before_uninstall"
# after_uninstall = "spherdex.uninstall.after_uninstall"

# Testing
# -------
# before_tests = "spherdex.install.before_tests"

# Overriding Methods
# ------------------------------
# override_whitelisted_methods = {
#     "frappe.desk.doctype.event.event.get_events": "spherdex.event.get_events"
# }

# Exempt linked doctypes from being automatically cancelled
# ---------------------------------------------------------
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# User Data Protection
# --------------------
# user_data_fields = [
#     {
#         "doctype": "Mitglied",
#         "filter_by": "owner",
#         "redact_fields": ["email", "phone"],
#         "partial": 1,
#     },
# ]

# Authentication and authorization
# --------------------------------
# auth_hooks = [
#     "spherdex.auth.validate"
# ]
