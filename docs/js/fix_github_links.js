document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("a[href*='github.com']").forEach(link => {
        link.setAttribute("target", "_blank");
        link.setAttribute("rel", "noopener noreferrer");
    });
});
