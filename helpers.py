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
    """Format the exercise id for onclick property of Add exercise button."""

    return f"addExercise({exercise_id}, event)"


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
