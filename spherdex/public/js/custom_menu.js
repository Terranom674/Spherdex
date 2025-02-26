$(document).ready(function () {
    // Prüfen, ob die Links bereits existieren
    if ($("#spherdex-links").length === 0) {
        let menuItem = $(`
            <div class="dropdown-divider"></div>
            <div id="spherdex-links">
                <a class="dropdown-item" href="/handbuch" target="_blank">📖 Handbuch (Lokal)</a>
                <a class="dropdown-item" href="https://terranom674.github.io/Spherdex" target="_blank">🌍 Handbuch (Online)</a>
                <a class="dropdown-item" href="https://github.com/Terranom674/Spherdex" target="_blank">🐙 Über Spherdex (GitHub Repository)</a>
            </div>
        `);

        // Menü in die bestehende Toolbar einfügen
        $("#toolbar-help").append(menuItem);
    }
});
