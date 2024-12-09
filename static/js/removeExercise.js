function removeExercise(exerciseNumber) {
  // Compose the exercise string
  const exerciseNumberString = `exercise-${exerciseNumber}`;

  // Get the exercise to remove
  const exercise = document.getElementById(exerciseNumberString);

  // Check if the exercise exists
  if (exercise) {
    exercise.remove();
  }

  // Re-index exercises
  reindexExercises();

  // Display the move buttons
  displayMoveButtons();
}

function reindexExercises() {
  // Get the exercises container
  const exercisesContainer = document.getElementById('exercises');

  // Loop through each exercise in the container
  Array.from(exercisesContainer.children).forEach((exercise, index) => {
    // Get the old exercise string
    const oldExerciseNumberString = exercise.getAttribute('id');

    // Determine the new exercise number
    const newExerciseNumber = index + 1;

    // Compose the new exercise string
    const newExerciseNumberString = `exercise-${newExerciseNumber}`;

    // Update ID of the exercise
    exercise.setAttribute('id', newExerciseNumberString);

    // Update the input with the exercise ID
    exercise.querySelector(`input[name="${oldExerciseNumberString}-id"]`)
      .setAttribute('name', `${newExerciseNumberString}-id`)

    // Update the input with the exercise rest time
    exercise.querySelector(`select[name="${oldExerciseNumberString}-rest"]`)
      .setAttribute('name', `${newExerciseNumberString}-rest`)

    // Update the Add set button
    const addSetButton = exercise.querySelector(`#${oldExerciseNumberString}-add-set`);
    addSetButton.setAttribute('id', `${newExerciseNumberString}-add-set`);
    addSetButton.setAttribute('onclick', `addSet('${newExerciseNumber}')`);

    // Update the Remove exercise button
    const removeExerciseButton = exercise
      .querySelector(`#${oldExerciseNumberString}-remove`);
    removeExerciseButton.setAttribute('id', `${newExerciseNumberString}-remove`);
    removeExerciseButton
      .setAttribute('onclick', `removeExercise('${newExerciseNumber}')`);

    // Update the Move up button
    const moveUpButton = exercise.querySelector(`#${oldExerciseNumberString}-move-up`);
    moveUpButton.setAttribute('id', `${newExerciseNumberString}-move-up`);
    moveUpButton.setAttribute('onclick', `moveExerciseUp('${newExerciseNumber}')`);

    // Update the Move down button
    const moveDownButton = exercise
      .querySelector(`#${oldExerciseNumberString}-move-down`);
    moveDownButton.setAttribute('id', `${newExerciseNumberString}-move-down`);
    moveDownButton.setAttribute('onclick', `moveExerciseDown('${newExerciseNumber}')`);

    // Update the sets container
    exercise.querySelector(`#${oldExerciseNumberString}-sets`)
      .setAttribute('id', `${newExerciseNumberString}-sets`);;

    // Re-index sets within the exercise
    reindexSets(newExerciseNumber);
  });
}
