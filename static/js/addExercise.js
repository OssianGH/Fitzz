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

  // Show loader
  document.getElementById('loader').classList.add('active');

  // Check if the exercise is already added
  if (checkAlreadyAdded(exerciseId)) {
    // Hide loader
    alert('Exercise already added.');
    document.getElementById('loader').classList.remove('active');
    return;
  }

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

    // Assign the class to the new exercise
    newExercise.setAttribute('class', 'exercise');

    // Assign a unique ID to the new exercise
    newExercise.setAttribute('id', exerciseNumberString);

    // Set the inner HTML of the new exercise
    newExercise.innerHTML = `
    <input id="${exerciseNumberString}-id" name="${exerciseNumberString}-id" type="hidden" value="${exercise.id}">
    <input id="${exerciseNumberString}-set-count" name="${exerciseNumberString}-set-count" type="hidden" value="0">
    <div class="exercise-name flex gap center-align between-justify">
      <div class="flex gap center-align">
        <div class="image-container">
          <img class="image" src="/static/images/exercises/${exercise.muscle_group.toLowerCase()}/${nameUnderscore}.png" alt="${exercise.name}">
        </div>
        <h3 class="h3 text-center no-margin">${exercise.name}</h3>
      </div>
      <div class="button-wrapper flex">
        <button class="square-btn" id="${exerciseNumberString}-add-set" type="button" onclick="addSet(${exerciseNumber})">
          <i class="fa fa-plus"></i>
        </button>
        <button class="square-btn" id="${exerciseNumberString}-remove" type="button" onclick="removeExercise(${exerciseNumber})">
          <i class="fa fa-trash"></i>
        </button>
        <button class="square-btn" id="${exerciseNumberString}-move-up" type="button" onclick="moveExerciseUp(${exerciseNumber})">
          <i class="fa fa-arrow-up"></i>
        </button>
        <button class="square-btn" id="${exerciseNumberString}-move-down" type="button" onclick="moveExerciseDown(${exerciseNumber})">
          <i class="fa fa-arrow-down"></i>
        </button>
      </div>
    </div>
    <div class="select-group">
      <label class="select-label">Rest time</label>
      <select class="input" id="${exerciseNumberString}-rest" name="${exerciseNumberString}-rest">
      </select>
    </div>
    <div id="${exerciseNumberString}-sets"></div>`;

    // Add the rest time options
    addRestTimeOptions(newExercise, exerciseNumberString);

    // Append the new exercise to the exercises container
    exercisesContainer.appendChild(newExercise);

    // Ingrease the exercise count
    const exerciseCountInput = document.getElementById('exercise-count');
    const exerciseCount = exerciseCountInput.value;
    exerciseCountInput.value = parseInt(exerciseCount, 10) + 1;

    // Add the first set
    addSet(exerciseNumber);

    // Display the move buttons
    displayMoveButtons();
  } catch (error) {
    console.error('Error:', error);
    alert('Failed to add exercise.');
  } finally {
    // Hide loader
    document.getElementById('loader').classList.remove('active');

    // Hide overlay
    document.getElementById('overlay').classList.remove('active');
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
    } else {
      moveUpButton.style.display = 'inline-block';
    }

    // Get the Move down button
    const moveDownButton = exercise.querySelector(`#${exerciseNumberString}-move-down`);

    // Check if the exercise is the last one
    if (exerciseNumber === exercisesContainer.childElementCount) {
      moveDownButton.style.display = 'none';
    } else {
      moveDownButton.style.display = 'inline-block';
    }
  });
}

function addRestTimeOptions(exerciseContainer, exerciseNumberString) {
  // Get the select element for the rest time
  const select = exerciseContainer.querySelector(`select[name="${exerciseNumberString}-rest"]`);

  // Create the rest time options from 5 to 300 seconds
  for (let i = 0; i <= 300; i += 5) {
    const newOption = document.createElement("option");
    newOption.value = `${i}`;
    newOption.text = formatSeconds(i);
    select.appendChild(newOption);
  }
}

function formatSeconds(seconds) {
  if (seconds < 60) {
    // Return the seconds if less than a minute
    return `${seconds} s`;
  }

  // Calculate the minutes
  const minutes = Math.floor(seconds / 60);

  // Calculate the remaining seconds
  const remainingSeconds = seconds % 60;

  // Return the formatted time in minutes and seconds
  return `${minutes} min ${remainingSeconds} s`;
}
