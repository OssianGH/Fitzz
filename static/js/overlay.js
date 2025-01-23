// Wait for DOM content to load
document.addEventListener('DOMContentLoaded', () => {
  // Add click event listener to the Add exercise button
  document.getElementById('add-exercise').addEventListener('click', showOverlay);

  // Add click event listener to the Show overlay button
  document.getElementById('hide-overlay').addEventListener('click', hideOverlay);
});

function showOverlay() {
  // Add active class to the overlay div
  document.getElementById('overlay').classList.add('active');
}

function hideOverlay() {
  // Remove active class to the overlay div
  document.getElementById('overlay').classList.remove('active');
}
