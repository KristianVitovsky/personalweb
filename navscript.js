
// Fetch and insert the navbar
/*   const navbarContainer = document.getElementById("navbarContainer");
fetch("navbar.html")
    .then(response => response.text())
    .then(data => {
        navbarContainer.innerHTML = data;
        addNavbarHoverListener();
    });

// Function to handle the hover event for the navbar
function addNavbarHoverListener() {
    const navbar = document.querySelector("nav");
    const mainContent = document.querySelector("main");

    mainContent.addEventListener("mouseleave", () => {
        navbar.classList.add("show");
    });

    mainContent.addEventListener("mouseenter", () => {
        navbar.classList.remove("show");
    });
}*/


fetch("navbar.html")
.then(response => response.text())
.then(data => {
    document.getElementById("navbar").innerHTML = data;
});