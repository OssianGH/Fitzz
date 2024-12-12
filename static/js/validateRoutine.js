// Wait for DOM content to load
document.addEventListener('DOMContentLoaded', () => {
  // Attach validation function to form submission
  document.getElementById('routine-form').addEventListener('submit', validateForm);
});


// Form validation function
function validateForm(event) {
  try {
    // Prevent form submission if validation fails
    event.preventDefault();

    // Access form routine name
    const routineName = document.getElementById('routine-name').value;

    // Ensure routine name was submitted
    if (!routineName) {
      alert('Routine name must be filled.');
      return;
    }

    // Access form exercise count
    const exerciseCount = parseInt(document.getElementById('exercise-count').value, 10);

    // Ensure the routine has at least one exercise
    if (exerciseCount < 1) {
      alert('There must be at least one exercise in the routine.');
      return;
    }

    // Loop through each exercise
    for (let i = 1; i <= exerciseCount; i++) {
      // Access form current exercise set count
      const setCount = parseInt(document.getElementById(`exercise-${i}-set-count`).value, 10);

      // Ensure the current exercise has at least one set
      if (setCount < 1) {
        alert(`Exercise ${i} must have at least one set.`);
        return;
      }

      // Access form current exercise rest time
      const restTime = document.getElementById(`exercise-${i}-rest`).value;

      // Validate exercise-x-rest (if filled)
      if (restTime) {
        // Ensure current exercise rest time is integer
        const restTimeValue = parseInt(restTime, 10);
        if (isNaN(restTimeValue)) {
          alert(`Exercise ${i} rest time must be an integer.`);
          return;
        }

        // Ensure current exercise rest time is positive
        if (restTimeValue < 0) {
          alert(`Exercise ${i} rest time must be positive.`);
          return;
        }

        // Ensure current exercise rest time is less than 300 seconds
        if (restTimeValue > 300) {
          alert(`Exercise ${i} rest time is too long.`);
          return;
        }

        // Ensure current exercise rest time is multiple of 5
        if (restTimeValue % 5 !== 0) {
          alert(`Exercise ${i} rest time is invalid.`);
          return;
        }
      }

      // Loop through each set of the current exercise
      for (let j = 1; j <= setCount; j++) {
        // Access form current set weight
        const weight = document.getElementById(`exercise-${i}-set-${j}-weight`).value;

        // Ensure current set weight was submitted
        if (!weight) {
          alert(`Mising exercise ${i} set ${j} weight.`);
          return;
        }

        // Ensure current set weight is integer
        const weightValue = parseInt(weight, 10);
        if (isNaN(weightValue)) {
          alert(`Exercise ${i} set ${j} weight must be an integer.`);
          return;
        }

        // Ensure current set weight is positive
        if (weightValue < 1) {
          alert(`Exercise ${i} set ${j} weight must be positive.`);
          return;
        }

        // Access form current set reps
        const reps = document.getElementById(`exercise-${i}-set-${j}-reps`).value;

        // Ensure current set reps was submitted
        if (!reps) {
          alert(`Mising exercise ${i} set ${j} reps.`);
          return;
        }

        // Ensure current set reps is integer
        const repsValue = parseInt(reps, 10);
        if (isNaN(repsValue)) {
          alert(`Exercise ${i} set ${j} reps must be an integer.`);
          return;
        }

        // Ensure current set reps is positive
        if (repsValue < 1) {
          alert(`Exercise ${i} set ${j} reps must be positive.`);
          return;
        }
      }
    }

    // Validaiton passed then submit form
    event.target.submit();
  } catch (error) {
    console.error(error);
    alert('An error occurred during form validation. Please try again.');
  }
}
