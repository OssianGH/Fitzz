// Wait for DOM content to load
document.addEventListener('DOMContentLoaded', () => {
  // Get the exercises container
  const exercisesContainer = document.getElementById('exercises');

  // Bind the animation for the new inputs to display animation 
  bindInputListeners();

  // Display the move buttons
  displayMoveButtons();

  // Loop through each exercise in the container
  Array.from(exercisesContainer.children).forEach((exercise, index) => {
    // Get the sets container
    const setsContainer = document.getElementById(`exercise-${index + 1}-sets`);

    // Get the number of child elements within the container
    const setsNumber = setsContainer.childElementCount

    // Check if there is no set in the container
    if (setsNumber === 0) {
      return
    }

    // Get the first set in the container
    const firstSet = setsContainer.children[0];

    // Check if there is more than one set in the container
    if (setsNumber > 1) {
      firstSet.querySelector('.square-btn').style.visibility = 'visible';
    } else {
      firstSet.querySelector('.square-btn').style.visibility = 'hidden';
    }
  });
});
