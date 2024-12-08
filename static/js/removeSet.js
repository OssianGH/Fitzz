function removeSet(exerciseNumber, setNumber) {
  // Compose the exercise string
  const exerciseNumberString = `exercise-${exerciseNumber}`;

  // Get the set to remove
  const set = document.getElementById(`${exerciseNumberString}-set-${setNumber}`);

  // Check if the set exists
  if (set) {
    set.remove();
  }

  // Re-index sets
  reindexSets(exerciseNumber);
}

function reindexSets(exerciseNumber) {
  // Compose the exercise string
  const exerciseNumberString = `exercise-${exerciseNumber}`;

  // Get the sets container
  const setsContainer = document.getElementById(`${exerciseNumberString}-sets`);

  // Loop through each set in the container
  Array.from(setsContainer.children).forEach((set, index) => {
    // Set the new set number
    const newSetNumber = index + 1;

    // Update the ID of the set
    set.setAttribute('id', `${exerciseNumberString}-set-${newSetNumber}`);

    // Update the set number
    set.querySelector('p').textContent = newSetNumber;

    // Loop through each input in the set
    set.querySelectorAll('input').forEach(input => {
      if (input.getAttribute('name').includes('-weight')) {
        // Update the weight input
        input.setAttribute('name', `${exerciseNumberString}-set-${newSetNumber}-weight`);
      } else if (input.getAttribute('name').includes('-reps')) {
        // Update the reps input
        input.setAttribute('name', `${exerciseNumberString}-set-${newSetNumber}-reps`)
      }
    });

    // Update the Remove set button
    set.querySelector('.square-btn').setAttribute('onclick', `removeSet(${exerciseNumber}, ${newSetNumber})`);
  });
}
