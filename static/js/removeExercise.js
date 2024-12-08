function removeExercise(exerciseNumber) {
  // Set the exercise string
  const exerciseNumberString = `exercise-${exerciseNumber}`;

  // Get the exercise to remove
  const exercise = document.getElementById(exerciseNumberString);

  // Check if the exercise exists
  if (exercise) {
    exercise.remove();
  }

  // Re-index exercises
  reindexExercises();
}


function reindexExercises() {
  // Set the exercise string
  const exercisesContainer = document.getElementById('exercises');

  Array.from(exercisesContainer.children).forEach((exercise, index) => {
    const oldExerciseNumberString = exercise.getAttribute('id');

    const newExerciseNumber = index + 1;
    const newExerciseNumberString = `exercise-${newExerciseNumber}`;

    // Update ID of the exercise
    exercise.setAttribute('id', newExerciseNumberString);

    // Update hidden input for exercise ID
    exercise.querySelector(`input[name="${oldExerciseNumberString}-id"]`).setAttribute('name', `${newExerciseNumberString}-id`)

    // Update the Add set button
    exercise.querySelector('.btn').setAttribute('onclick', `addSet('${newExerciseNumber}')`);

    // Update the sets container
    exercise.querySelector(`#${oldExerciseNumberString}-sets`).setAttribute('id', `${newExerciseNumberString}-sets`);;

    // Re-index sets within the exercise
    reindexSets(newExerciseNumber);
  });
}