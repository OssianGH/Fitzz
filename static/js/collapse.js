// Wait for DOM content to load
document.addEventListener('DOMContentLoaded', onContentLoad);

function onContentLoad(event) {
  // Add event listener to the collapse button
  document.getElementById("collapse-toggle").addEventListener("click", collapseToggle);
}

// Toggle the navbar menu
function collapseToggle() {
  const nav = document.getElementById("navbar")
  nav.classList.toggle("active");
}