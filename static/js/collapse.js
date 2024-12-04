// Wait for DOM content to load
document.addEventListener('DOMContentLoaded', () => {
  // Add click event listener to the Toggle nav button
  document.getElementById('toggle-nav').addEventListener('click', toggleNav);
});

const toggleNav = () => {
  // Get the nav element
  const navElement = document.getElementById('nav');

  // Toggle the nav element visibility
  navElement.classList.toggle('active');
}
