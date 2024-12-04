// Wait for DOM content to load
document.addEventListener('DOMContentLoaded', onContentLoad);


function onContentLoad(event) {
  // Select all input elements with the class 'input'
  const inputs = document.querySelectorAll('.input-group .input');

  // Loop through each input
  inputs.forEach(input => {
    // Add focus event listener to the input
    input.addEventListener('focus', () => {
      // Add active class to the input
      input.classList.add('active');
    });

    // Add blur event listener to the input
    input.addEventListener('blur', () => {
      if (!input.value) {
        // Remove active class to the input if is empty
        input.classList.remove('active');
      }
    });
  });
}
