document.body.classList.add("fade-in");
nav = document.querySelectorAll(".nav-item");
selected = document.getElementById("nav-selected");

selected.style.color = "black";
selected.style.backgroundColor = "#ffae89";
selected.style.borderRadius = "10px"

nav.forEach(function(navItem) {
    navItem.addEventListener("mouseover", changeStyle);
    navItem.addEventListener("mouseout", revertStyle);
    navItem.addEventListener("click", navItemClick);
    navItem.style.padding = "10px";
});

function changeStyle(event) {
    if(event.target.id == "nav-selected") return;
    event.target.style.color = "black";
    event.target.style.backgroundColor = "#ffae89";
    event.target.style.borderRadius = "10px";
    event.target.style.transform = "scale(1.2)";
    event.target.style.transition = "all 0.8s ease";
}

function revertStyle(event) {
    if(event.target.id == "nav-selected") return;
    event.target.style.color = "#ff4f00";
    event.target.style.backgroundColor = "white";
    event.target.style.transform = "scale(1)";
    event.target.style.transition = "all 1s ease";
}

function navItemClick(event) {
    if(event.target.id == "nav-selected") return;
    event.preventDefault();
    var target = this.getAttribute("href");
    document.body.classList.add("fade-out");
    setTimeout(function() {
        window.location.href = target;
    }, 100);
}