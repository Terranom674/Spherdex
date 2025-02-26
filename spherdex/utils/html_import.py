import os
import re
from werkzeug.wrappers import Response
import frappe

def serve_search_index():
    """Liefert `search_index.json` direkt aus."""
    file_path = os.path.join(frappe.get_app_path("spherdex"), "public", "docs", "search", "search_index.json")

    if not os.path.exists(file_path):
        return Response("File not found", status=404, content_type="application/json")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return Response(content, content_type="application/json")

def handle_special_requests(requested_page):
    """Prüft, ob `search_index.json` oder eine andere Spezialanfrage vorliegt."""
    if requested_page == "search/search_index.json":
        return serve_search_index()
    return None

def load_page(page_name="index.html"):
    """Lädt die gewünschte HTML-Seite aus dem Handbuch-Verzeichnis."""
    file_path = os.path.join(frappe.get_app_path("spherdex"), "public", "docs", page_name)

    if not os.path.exists(file_path):
        return "<h1>Seite nicht gefunden: {}</h1>".format(page_name)

    with open(file_path, "r", encoding="utf-8") as f:
        handbuch_html = f.read()

    handbuch_html = fix_resource_paths(handbuch_html)
    return inject_styles_and_scripts(handbuch_html)

def fix_resource_paths(html_content):
    """Korrigiert Ressourcen-Pfade für CSS, JS, Bilder."""
    html_content = html_content.replace('href="assets/', 'href="/assets/spherdex/docs/assets/')
    html_content = html_content.replace('src="js/', 'src="/assets/spherdex/docs/js/')
    html_content = html_content.replace('src="img/', 'src="/assets/spherdex/docs/img/')
    html_content = html_content.replace('src="assets/javascripts/', 'src="/assets/spherdex/docs/assets/javascripts/')
    html_content = html_content.replace('src="assets/images/', 'src="/assets/spherdex/docs/assets/images/')
    return html_content

def inject_styles_and_scripts(html_content):
    """Fügt das globale CSS und das JavaScript zur Link-Korrektur in die Seite ein."""
    return html_content.replace(
        "<head>",
        '''<head>
        <link rel="stylesheet" type="text/css" href="/assets/spherdex/css/handbook.css">
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                document.querySelectorAll('a[href]').forEach(function(link) {
                    var href = link.getAttribute("href");

                    // ✅ Falls der Link relativ ist UND nicht zu `/assets/` gehört, konvertiere ihn in `/test/`
                    if (href && !href.startsWith("http") && !href.startsWith("#") && !href.startsWith("/assets/") && href.indexOf("?page=") === -1) {
                        link.setAttribute("href", "/test/" + href);
                    }
                });
            });

            (function() {
                var originalFetch = window.fetch;
                window.fetch = function(url, options) {
                    if (typeof url === "string" && url.includes("search/search_index.json")) {
                        return fetch("/assets/spherdex/docs/search/search_index.json", options);
                    }
                    return originalFetch(url, options);
                };

                var originalXHR = window.XMLHttpRequest;
                window.XMLHttpRequest = function() {
                    var xhr = new originalXHR();
                    var originalOpen = xhr.open;
                    var originalSend = xhr.send;

                    xhr.open = function(method, url, async, user, password) {
                        if (url.includes("search/search_index.json")) {
                            arguments[1] = "/assets/spherdex/docs/search/search_index.json";
                        }
                        return originalOpen.apply(this, arguments);
                    };

                    xhr.send = function(body) {
                        return originalSend.apply(this, arguments);
                    };

                    return xhr;
                };
            })();
        </script>'''
    )

def get_page_context(context, default_page="index.html"):
    """Zentrale Steuerung für das Laden von HTML-Seiten und Spezialanfragen."""
    
    if context is None:
        context = {}

    # ✅ Request-Pfad bereinigen
    requested_page = frappe.local.request.path.strip("/")

    # ✅ Prüfe auf Spezialanfragen (z. B. `search_index.json`)
    special_response = handle_special_requests(requested_page)
    if special_response:
        return special_response

    # ✅ Standardseite laden (z. B. `index.html`)
    context["handbuch_html"] = load_page(default_page)
    return context