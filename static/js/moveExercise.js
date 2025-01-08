function moveExerciseUp(exerciseNumber) {
  // Get the exercises container
  const exercisesContainer = document.getElementById('exercises');

  // Compose the exercise string
  const exerciseNumberString = `exercise-${exerciseNumber}`;

  // Get the exercise to move
  const exercise = document.getElementById(exerciseNumberString);

  // Get the previous exercise
  const prevExercise = exercise.previousElementSibling;

  // Check if there is no previous exercise
  if (!prevExercise) {
    return
  }

  // Insert the exercise before the previos
  exercisesContainer.insertBefore(exercise, prevExercise)

  // Re-index exercises
  reindexExercises();

  // Display the move buttons
  displayMoveButtons();
}

function moveExerciseDown(exerciseNumber) {
  // Get the exercises container
  const exercisesContainer = document.getElementById('exercises');

  // Compose the exercise string
  const exerciseNumberString = `exercise-${exerciseNumber}`;

  // Get the exercise to move
  const exercise = document.getElementById(exerciseNumberString);

  // Get the next exercise
  const nextExercise = exercise.nextElementSibling;

  // Check if there is no next exercise
  if (!nextExercise) {
    return
  }

  // Insert exercise after the next
  exercisesContainer.insertBefore(nextExercise, exercise);

  // Re-index exercises
  reindexExercises();

  // Display the move buttons
  displayMoveButtons();
}
