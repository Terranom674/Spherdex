import os
from werkzeug.wrappers import Response

def get_context(context):
    """Lädt die Installation-Seite für `/test/installation.html`."""

    if context is None:
        context = {}

    # Lade die entsprechende HTML-Seite
    file_path = os.path.join(os.path.dirname(__file__), "installation.html")

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            context["handbuch_html"] = f.read()
        return context

    # Falls die Datei nicht existiert, zeige eine Fehlermeldung
    context["handbuch_html"] = "<h1>Seite nicht gefunden: installation.html</h1>"
    return context
