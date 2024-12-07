async function addExercise(exerciseId, event) {
  event.preventDefault();

  // Remove active class to the overlay div
  document.getElementById('overlay').classList.remove('active');

  try {
    const response = await fetch(`/exercise/${exerciseId}`);

    if (!response.ok) {
      throw new Error('Exercise not found');
    }

    const exercise = await response.json();

    // Replace spaces with underscores in the exercise name
    name_underscore = exercise.name.toLowerCase().replace(/ /g, "_");

    // Create a new exercise element
    const newExercise = document.createElement("div");

    // Assign a unique ID to the new exercise
    newExercise.id = `exercise-${exercise.id}`;

    // Assign the class name to the new exercise
    newExercise.className = "exercise";

    // Set the inner HTML of the new exercise
    newExercise.innerHTML = `
    <div class="exercise-name flex center-align between-justify">
      <div class="image-container">
        <img class="image" src="/static/images/exercises/${exercise.muscle_group.toLowerCase()}/${name_underscore}.png" alt="${exercise.name}">
      </div>
      <h3 class="h3 text-center no-margin">${exercise.name}</h3>
      <button id="add-set" class="btn" type="button">Add set</button>
    </div>
    <div id="set-1" class="exercise-set flex gap center-align">
      <p class="no-margin">1</p>
      <div class="input-wrapper flex gap center-align evenly-justify">
        <div class="input-group">
          <input class="input" autocomplete="off" name="weight" type="text">
          <label class="input-label">Weight</label>
        </div>
        <div class="input-group">
          <input class="input" autocomplete="off" name="reps" type="text">
          <label class="input-label">Reps</label>
        </div>
      </div>
    </div>`;

    // newExercise.querySelector("#add-set").addEventListener("click", addSet);

    const exercisesContainer = document.getElementById("exercises");

    // Append the new exercise to the exercises container
    exercisesContainer.appendChild(newExercise);
    window.bindInputListeners();


  } catch (error) {
    console.error('Error:', error);
    alert('Failed to add exercise.');
  }
}
