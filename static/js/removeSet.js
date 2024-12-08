function removeSet(exerciseNumber, setNumber) {
  // Set the exercise string
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
  const exerciseNumberString = `exercise-${exerciseNumber}`;

  const setsContainer = document.getElementById(`${exerciseNumberString}-sets`);

  Array.from(setsContainer.children).forEach((set, index) => {
    const newSetNumber = index + 1;

    set.setAttribute('id', `${exerciseNumberString}-set-${newSetNumber}`);

    set.querySelector('p').textContent = newSetNumber;

    set.querySelectorAll('input').forEach(input => {
      if (input.name.includes('-weight')) {
        input.name = `${exerciseNumberString}-set-${newSetNumber}-weight`;
      } else if (input.name.includes('-reps')) {
        input.name = `${exerciseNumberString}-set-${newSetNumber}-reps`;
      }
    });

    set.querySelector('.square-btn').setAttribute('onclick', `removeSet(${exerciseNumber}, ${newSetNumber})`);
  });
}
