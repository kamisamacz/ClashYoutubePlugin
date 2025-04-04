const OVERLAY_URL = "http://192.168.88.45:8000/overlay/";

function injectOverlay() {
    if (document.getElementById("clash-overlay-frame")) return;

    const iframe = document.createElement("iframe");
    iframe.src = OVERLAY_URL;
    iframe.id = "clash-overlay-frame";
    iframe.style.position = "absolute";
    iframe.style.top = "0";
    iframe.style.left = "0";
    iframe.style.width = "100%";
    iframe.style.height = "100%";
    iframe.style.zIndex = "9999";
    iframe.style.pointerEvents = "none";
    iframe.style.border = "none";
    iframe.style.background = "transparent";

    const player = document.getElementById("movie_player") || document.querySelector("#player");
    if (player) {
        player.style.position = "relative";
        player.appendChild(iframe);
    }
}
injectOverlay();
