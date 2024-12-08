function checkAlreadyAdded(exerciseId) {
  // Get the exercises container
  const exercisesContainer = document.getElementById('exercises');

  // Loop through each exercise in the container
  for (let index = 0; index < exercisesContainer.children.length; index++) {
    // Get the current exercise
    const exercise = exercisesContainer.children[index];

    // Determine the exercise number
    const exerciseNumber = index + 1;

    // Compose the exercise string
    const exerciseNumberString = `exercise-${exerciseNumber}`;

    // Get the input with the exercise ID
    const input = exercise.querySelector(`input[name="${exerciseNumberString}-id"]`);

    // Check if the input exists and the value matches the exercise ID
    if (input && input.value === `${exerciseId}`) {
      return true;
    }
  }

  return false;
}

async function addExercise(exerciseId, event) {
  // Prevent the default anchor tag behavior
  event.preventDefault();

  // Check if the exercise is already added
  if (checkAlreadyAdded(exerciseId)) {
    alert('Exercise already added.');
    return;
  }

  // Hide overlay
  document.getElementById('overlay').classList.remove('active');

  try {
    // Fetch the exercise data
    const response = await fetch(`/exercise/${exerciseId}`);

    // Check if the response is not OK
    if (!response.ok) {
      throw new Error('Exercise not found');
    }

    // Parse the JSON response
    const exercise = await response.json();

    // Get the exercises container
    const exercisesContainer = document.getElementById('exercises');

    // Get the number of exercises in the container
    const exerciseNumber = exercisesContainer.childElementCount + 1;

    // Compose the exercise string
    const exerciseNumberString = `exercise-${exerciseNumber}`;

    // Replace spaces with underscores in the exercise name
    const nameUnderscore = exercise.name.toLowerCase().replace(/ /g, '_');

    // Create the new exercise div
    const newExercise = document.createElement('div');

    // Assign a unique ID to the new exercise
    newExercise.setAttribute('id', exerciseNumberString);

    // Assign the class to the new exercise
    newExercise.setAttribute('class', 'exercise');

    // Set the inner HTML of the new exercise
    newExercise.innerHTML = `
    <input type="hidden" name="${exerciseNumberString}-id" value="${exercise.id}">
    <div class="exercise-name flex gap center-align between-justify">
      <div class="flex gap center-align">
        <div class="image-container">
          <img class="image" src="/static/images/exercises/${exercise.muscle_group.toLowerCase()}/${nameUnderscore}.png" alt="${exercise.name}">
        </div>
        <h3 class="h3 text-center no-margin">${exercise.name}</h3>
      </div>
      <div class="button-wrapper flex">
        <button id=${exerciseNumberString}-add-set class="square-btn" type="button" onclick="addSet(${exerciseNumber})">
          <i class="fa fa-plus"></i>
        </button>
        <button id=${exerciseNumberString}-remove class="square-btn" type="button" onclick="removeExercise(${exerciseNumber})">
          <i class="fa fa-trash"></i>
        </button>
        <button id=${exerciseNumberString}-move-up class="square-btn" type="button" onclick="moveExerciseUp(${exerciseNumber})">
          <i class="fa fa-arrow-up"></i>
        </button>
        <button id=${exerciseNumberString}-move-down class="square-btn" type="button" onclick="moveExerciseDown(${exerciseNumber})">
          <i class="fa fa-arrow-down"></i>
        </button>
      </div>
    </div>
    <div id="${exerciseNumberString}-sets"></div>`;

    // Append the new exercise to the exercises container
    exercisesContainer.appendChild(newExercise);

    // Add the first set
    addSet(exerciseNumber);

    // Display the move buttons
    displayMoveButtons();

    // Bind the animation for the new inputs to display animation 
    window.bindInputListeners();
  } catch (error) {
    console.error('Error:', error);
    alert('Failed to add exercise.');
  }
}

function displayMoveButtons() {
  // Get the exercises container
  const exercisesContainer = document.getElementById('exercises');

  // Loop through each exercise in the container
  Array.from(exercisesContainer.children).forEach((exercise, index) => {
    // Determine the exercise number
    const exerciseNumber = index + 1;

    // Compose the exercise string
    const exerciseNumberString = `exercise-${exerciseNumber}`;

    // Get the Move up button
    const moveUpButton = exercise.querySelector(`#${exerciseNumberString}-move-up`);

    // Check if the exercise is the first one
    if (exerciseNumber === 1) {
      moveUpButton.style.display = 'none';
    }
    else {
      moveUpButton.style.display = 'inline-block';
    }

    // Get the Move down button
    const moveDownButton = exercise.querySelector(`#${exerciseNumberString}-move-down`);

    // Check if the exercise is the last one
    if (exerciseNumber === exercisesContainer.childElementCount) {
      moveDownButton.style.display = 'none';
    }
    else {
      moveDownButton.style.display = 'inline-block';
    }
  });
}
