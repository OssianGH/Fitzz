// Wait for DOM content to load
document.addEventListener('DOMContentLoaded', () => {
  // Get the Toggle nav button
  const toggleNavButton = document.getElementById('toggle-nav');

  // Check the Toggle nav button exist
  if (!toggleNavButton) {
    return;
  }

  // Add click event listener to the Toggle nav button
  toggleNavButton.addEventListener('click', toggleNav);
});

const toggleNav = () => {
  // Get the nav element
  const navElement = document.getElementById('nav');

  // Toggle the nav element visibility
  navElement.classList.toggle('active');
}
