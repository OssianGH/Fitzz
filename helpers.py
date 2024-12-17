from flask import redirect, render_template, session
from functools import wraps


def display_error(message=""):
    """Render message as an error to user."""

    if not message:
        message = """The server encountered an internal error and was unable to complete
                your request."""

    return render_template("error.html", message=message)


def exercise_image(name, muscle_group):
    """Get an exercise image path given its name and muscle group."""

    exercises_path = "/static/images/exercises"

    name = name.lower().replace(" ", "_")
    muscle_group = muscle_group.lower()

    return f"{exercises_path}/{muscle_group}/{name}.png"


def format_add_exercise(exercise_id):
    """Format text for onclick property of Add exercise button."""

    return f"addExercise({exercise_id}, event)"


def format_add_set(exercise_number):
    """Format text for onclick property of Add set button."""

    return f"addSet({exercise_number})"


def format_move_exercise_down(exercise_number):
    """Format text for onclick property of Move exercise down button."""

    return f"moveExerciseDown({exercise_number})"


def format_move_exercise_up(exercise_number):
    """Format text for onclick property of Move exercise up button."""

    return f"moveExerciseUp({exercise_number})"


def format_remove_exercise(exercise_number):
    """Format text for onclick property of Remove exercise button."""

    return f"removeExercise({exercise_number})"


def format_remove_set(exercise_number, set_number):
    """Format text for onclick property of Remove set button."""

    return f"removeSet({exercise_number}, {set_number})"


def format_seconds(seconds):
    """Format seconds to string of minutes and seconds."""

    if seconds < 60:
        # Return the seconds if less than a minute
        return f"{seconds} s"

    # Calculate the minutes
    minutes = seconds // 60

    # Calculate the remaining seconds
    remaining_seconds = seconds % 60

    # Return the formatted time in minutes and seconds
    return f"{minutes} min {remaining_seconds} s"


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def muscle_group_image(name):
    """Get an muscle group image path given its name."""

    muscle_group_path = "/static/images/exercises/types"

    name = name.lower()

    return f"{muscle_group_path}/{name}.png"
