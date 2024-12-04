// Wait for DOM content to load
document.addEventListener('DOMContentLoaded', onContentLoad);

function onContentLoad(event) {
  // Add event listener to the add set button
  document.getElementById('add-set').addEventListener('click', addSet)
}

const addSet = () => {
  // Create the set div
  const div = document.createElement('div')
  div.classList.add('exercise-set')
  div.classList.add('flex')
  div.classList.add('gap')
  div.classList.add('center-align')
  div.innerHTML = `
  <p class="text-center no-margin">1</p>
  <div class="input-wrapper flex gap center-align evenly-justify">
  <div class="input-group">
  <input class="input" autocomplete="off" name="routine-name" type="text">
  <label for="name" class="input-label">Weight</label>
  </div>
  <div class="input-group">
  <input class="input" autocomplete="off" name="routine-name" type="text">
  <label for="name" class="input-label">Reps</label>
  </div>
  </div>`

  // Append the set div to the exercise-1 div
  document.getElementById('exercise-1').appendChild(div)
}