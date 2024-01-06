function showPopup(url) {
    var popup = document.getElementById("popup-modal");
    var content = document.getElementById("popup-content");
    var iframe = document.createElement("iframe");
    iframe.src = url;
    iframe.style.width = "100%";
    iframe.style.height = "100%";
    content.innerHTML = "";
    content.appendChild(iframe);
    popup.style.display = "block";
}

function hidePopup() {
    var popup = document.getElementById("popup-modal");
    popup.style.display = "none";
}