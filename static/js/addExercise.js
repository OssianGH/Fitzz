async function addExercise(exerciseId, event) {
  // Prevent the default anchor tag behavior
  event.preventDefault();

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
      <div class="image-container">
        <img class="image" src="/static/images/exercises/${exercise.muscle_group.toLowerCase()}/${nameUnderscore}.png" alt="${exercise.name}">
      </div>
      <h3 class="h3 text-center no-margin">${exercise.name}</h3>
      <div class="button-wrapper flex between-justify">
        <button id=${exerciseNumberString}-add-set class="square-btn" type="button" onclick="addSet(${exerciseNumber})">
          <i class="fa fa-plus"></i>
        </button>
        <button id=${exerciseNumberString}-remove class="square-btn" type="button" onclick="removeExercise(${exerciseNumber})">
          <i class="fa fa-trash"></i>
        </button>
      </div>
    </div>
    <div id="${exerciseNumberString}-sets">
      <div id="${exerciseNumberString}-set-1" class="exercise-set flex gap center-align">
        <p class="no-margin">1</p>
        <div class="input-wrapper flex gap center-align evenly-justify">
          <div class="input-group">
            <input class="input" autocomplete="off" name="${exerciseNumberString}-set-1-weight" type="text">
            <label class="input-label">Weight</label>
          </div>
          <div class="input-group">
            <input class="input" autocomplete="off" name="${exerciseNumberString}-set-1-reps" type="text">
            <label class="input-label">Reps</label>
          </div>
        </div>
        <button class="square-btn" type="button" onclick="removeSet(${exerciseNumber}, 1)">
          <i class="fa fa-trash"></i>
        </button>
      </div>
    </div>`;

    // Append the new exercise to the exercises container
    exercisesContainer.appendChild(newExercise);

    // Bind the animation for the new inputs to display animation 
    window.bindInputListeners();
  } catch (error) {
    console.error('Error:', error);
    alert('Failed to add exercise.');
  }
}
