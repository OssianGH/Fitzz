function removeExercise(exerciseNumber) {
  // Compose the exercise string
  const exerciseNumberString = `exercise-${exerciseNumber}`;

  // Get the exercise to remove
  const exercise = document.getElementById(exerciseNumberString);

  // Check if the exercise exists
  if (exercise) {
    exercise.remove();
  }

  // Decrease the exercise count
  const exerciseCountInput = document.getElementById('exercise-count')
  const exerciseCount = exerciseCountInput.value
  exerciseCountInput.value = parseInt(exerciseCount, 10) - 1

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

    // Update ID of the exercise container
    exercise.setAttribute('id', newExerciseNumberString);

    // Update the input with the ID of the exercise
    const idInput = exercise.querySelector(`#${oldExerciseNumberString}-id`);
    idInput.setAttribute('id', `${newExerciseNumberString}-id`);
    idInput.setAttribute('name', `${newExerciseNumberString}-id`);

    const setCountInput = exercise
      .querySelector(`#${oldExerciseNumberString}-set-count`);
    setCountInput.setAttribute('id', `${newExerciseNumberString}-set-count`);
    setCountInput.setAttribute('name', `${newExerciseNumberString}-set-count`);

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

    // Update the input with the exercise rest time
    const restTimeSelect = exercise.querySelector(`#${oldExerciseNumberString}-rest`);
    restTimeSelect.setAttribute('id', `${newExerciseNumberString}-rest`);
    restTimeSelect.setAttribute('name', `${newExerciseNumberString}-rest`);

    // Update the sets container
    const setsContainer = exercise.querySelector(`#${oldExerciseNumberString}-sets`);
    setsContainer.setAttribute('id', `${newExerciseNumberString}-sets`);

    // Re-index sets within the exercise
    reindexSets(newExerciseNumber);
  });
}
