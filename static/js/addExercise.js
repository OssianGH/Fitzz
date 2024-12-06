// Wait for DOM content to load
document.addEventListener('DOMContentLoaded', () => {
  // Add click event listener to the Add exercise button
  document.getElementById('add-exercise').addEventListener('click', addExercise);
});

function addExercise() {
  // Get the exercises container
  const exercisesContainer = document.getElementById("exercises");

  // Get the number of exercises in the container
  const exerciseCount = exercisesContainer.childElementCount + 1;

  // Create a new exercise element
  const newExercise = document.createElement("div");

  // Assign a unique ID to the new exercise
  newExercise.id = `exercise-${exerciseCount}`;

  // Assign the class name to the new exercise
  newExercise.className = "exercise";

  // Set the inner HTML of the new exercise
  newExercise.innerHTML = `
  <div class="exercise">
    <div class="exercise-name flex center-align between-justify">
      <img class="exercise-image" src="/static/images/barbell_bench_press.png">
      <h3 class="h3 text-center no-margin">Barbell Bench Press</h3>
      <button id="add-set" class="btn" type="button">Add set</button>
    </div>
    <div id="set-1" class="exercise-set flex gap center-align">
      <p class="text-center no-margin">1</p>
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
    </div>
  </div>
  `;

  // newExercise.querySelector("#add-set").addEventListener("click", addSet);

  // Append the new exercise to the exercises container
  exercisesContainer.appendChild(newExercise);
  window.bindInputListeners();
}
