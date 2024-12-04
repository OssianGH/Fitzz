// Wait for DOM content to load
document.addEventListener('DOMContentLoaded', onContentLoad);

function onContentLoad(event) {
  // Add event listener to the collapse button
  document.getElementById("collapse-toggle").addEventListener("click", collapseToggle);
}

function collapseToggle() {
  // Select the navbar element
  const nav = document.getElementById("navbar")

  // Toggle the navbar menu
  nav.classList.toggle("active");
}