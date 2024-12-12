function removeSet(exerciseNumber, setNumber) {
  // Compose the exercise string
  const exerciseNumberString = `exercise-${exerciseNumber}`;

  // Get the sets container
  const setsContainer = document.getElementById(`${exerciseNumberString}-sets`);

  // Check if there is only one set in the container
  if (setsContainer.childElementCount === 1) {
    return;
  }

  // Get the set to remove
  const set = document.getElementById(`${exerciseNumberString}-set-${setNumber}`);

  // Check if the set exists
  if (set) {
    set.remove();
  }

  // Decrease the set count for this exercise
  const setCountInput = document.getElementById(`${exerciseNumberString}-set-count`);
  const setCount = setCountInput.value;
  setCountInput.value = parseInt(setCount, 10) - 1;

  // Re-index sets
  reindexSets(exerciseNumber);

  // Display the first remove set button
  displayFirstRemoveSetButton(exerciseNumber);
}

function reindexSets(exerciseNumber) {
  // Compose the exercise string
  const exerciseNumberString = `exercise-${exerciseNumber}`;

  // Get the sets container
  const setsContainer = document.getElementById(`${exerciseNumberString}-sets`);

  // Loop through each set in the container
  Array.from(setsContainer.children).forEach((set, index) => {
    // Get the old set string
    const oldSetString = set.getAttribute('id');

    // Determine the new set number
    const newSetNumber = index + 1;

    // Update the ID of the set
    set.setAttribute('id', `${exerciseNumberString}-set-${newSetNumber}`);

    // Update the set number
    const setLabel = set.querySelector(`#${oldSetString}-label`);
    setLabel.setAttribute('id', `${exerciseNumberString}-set-${newSetNumber}-label`);
    setLabel.textContent = newSetNumber;

    // Update the weight input
    const weightInput = set.querySelector(`#${oldSetString}-weight`);
    weightInput
      .setAttribute('id', `${exerciseNumberString}-set-${newSetNumber}-weight`);
    weightInput
      .setAttribute('name', `${exerciseNumberString}-set-${newSetNumber}-weight`);

    // Update the reps input
    const repsInput = set.querySelector(`#${oldSetString}-reps`);
    repsInput.setAttribute('id', `${exerciseNumberString}-set-${newSetNumber}-reps`);
    repsInput.setAttribute('name', `${exerciseNumberString}-set-${newSetNumber}-reps`);

    // Update the Remove set button
    const removeSetButton = set.querySelector(`#${oldSetString}-remove`);
    removeSetButton.setAttribute('id', `${exerciseNumberString}-set-${newSetNumber}-remove`);
    removeSetButton.setAttribute('onclick', `removeSet(${exerciseNumber}, ${newSetNumber})`);
  });
}
