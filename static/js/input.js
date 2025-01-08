// Wait for DOM content to load
document.addEventListener('DOMContentLoaded', () => {
  // Bind event listeners initially
  bindInputListeners();
});

function bindInputListeners() {
  // Select all elements with the class 'input' inside the class 'input-group'
  const inputs = document.querySelectorAll('.input-group .input');

  // Loop through each input
  inputs.forEach(input => {
    // Add focus event listener to the current input
    input.addEventListener('focus', () => {
      // Add active class to the input
      input.classList.add('active');
    });

    // Add blur event listener to the current input
    input.addEventListener('blur', () => {
      if (!input.value) {
        // Remove active class to the input if it's empty
        input.classList.remove('active');
      }
    });
  });
}
