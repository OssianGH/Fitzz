function addSet(exerciseNumber) {
  // Compose the exercise string
  const exerciseNumberString = `exercise-${exerciseNumber}`;

  // Get the sets container
  const setsContainer = document.getElementById(`${exerciseNumberString}-sets`);

  // Get the number of sets in the container
  const setNumber = setsContainer.childElementCount + 1;

  // Create the new set div
  const newSet = document.createElement('div');

  // Assign the class name to the new set
  newSet.setAttribute('class', 'exercise-set flex gap center-align')

  // Assign a unique ID to the new set
  newSet.setAttribute('id', `${exerciseNumberString}-set-${setNumber}`);

  // Set the inner HTML of the new set
  newSet.innerHTML = `
  <p class="no-margin" id="${exerciseNumberString}-set-${setNumber}-label">${setNumber}</p>
  <div class="input-wrapper flex gap center-align evenly-justify">
    <div class="input-group">
      <input class="input" id="${exerciseNumberString}-set-${setNumber}-weight" name="${exerciseNumberString}-set-${setNumber}-weight" type="number" autocomplete="off" min="1">
      <label class="input-label">Weight</label>
    </div>
    <div class="input-group">
      <input class="input" id="${exerciseNumberString}-set-${setNumber}-reps" name="${exerciseNumberString}-set-${setNumber}-reps" type="number" autocomplete="off" min="1">
      <label class="input-label">Reps</label>
    </div>
  </div>
  <button class="square-btn" id="${exerciseNumberString}-set-${setNumber}-remove" type="button" onclick="removeSet(${exerciseNumber}, ${setNumber})">
    <i class="fa fa-trash"></i>
  </button>`;

  // Append new set to the sets container
  setsContainer.appendChild(newSet);

  // Increase the set count for this exercise
  const setCountInput = document.getElementById(`${exerciseNumberString}-set-count`);
  const setCount = setCountInput.value;
  setCountInput.value = parseInt(setCount, 10) + 1;

  // Display the first remove set button
  displayFirstRemoveSetButton(exerciseNumber);

  // Bind the animation for the new inputs to display animation
  bindInputListeners();
}

function displayFirstRemoveSetButton(exerciseNumber) {
  // Compose the exercise string
  const exerciseNumberString = `exercise-${exerciseNumber}`;

  // Get the sets container
  const setsContainer = document.getElementById(`${exerciseNumberString}-sets`);

  // Get the number of child elements within the container
  const setsNumber = setsContainer.childElementCount

  // Check if there is no set in the container
  if (setsNumber === 0) {
    return
  }

  // Get the first set in the container
  const firstSet = setsContainer.children[0];

  // Check if there is more than one set in the container
  if (setsNumber > 1) {
    firstSet.querySelector('.square-btn').style.visibility = 'visible';
  } else {
    firstSet.querySelector('.square-btn').style.visibility = 'hidden';
  }
}
