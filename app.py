import os

from cs50 import SQL
from collections import defaultdict
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import (
    display_error,
    exercise_image,
    format_add_exercise,
    format_add_set,
    format_move_exercise_down,
    format_move_exercise_up,
    format_remove_exercise,
    format_remove_set,
    format_seconds,
    login_required,
    muscle_group_image,
)

# Configure application
app = Flask(__name__)

# Custom filters
app.jinja_env.filters["exercise_image"] = exercise_image
app.jinja_env.filters["format_add_exercise"] = format_add_exercise
app.jinja_env.filters["format_add_set"] = format_add_set
app.jinja_env.filters["format_move_exercise_down"] = format_move_exercise_down
app.jinja_env.filters["format_move_exercise_up"] = format_move_exercise_up
app.jinja_env.filters["format_remove_exercise"] = format_remove_exercise
app.jinja_env.filters["format_remove_set"] = format_remove_set
app.jinja_env.filters["format_seconds"] = format_seconds
app.jinja_env.filters["muscle_group_image"] = muscle_group_image

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///fitzz.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show welcome page"""

    # Query database for username
    user = db.execute("SELECT username FROM user WHERE id = ?", session["user_id"])[0]

    # Query database for all user's routines
    routine_names = db.execute(
        "SELECT id, name FROM routine WHERE user_id = ?", session["user_id"]
    )

    # Map routine IDs to their names
    routine_map = {routine["id"]: routine["name"] for routine in routine_names}

    # Query database for all exercises in user's routines
    exercises = db.execute(
        """
            SELECT
                r.id AS routine_id,
                e.name AS exercise_name
            FROM routine r
            JOIN routine_exercise re ON r.id = re.routine_id
            JOIN exercise e ON re.exercise_id = e.id
            WHERE r.user_id = ?
            ORDER BY r.id, re.position
        """,
        session["user_id"],
    )

    # Create a dictionary to store exercises by routine
    routine_exercises = defaultdict(list)

    # Loop through exercises in each routine
    for exercise in exercises:
        # Add exercise to the dictionary on the corresponding routine ID
        routine_exercises[exercise["routine_id"]].append(exercise["exercise_name"])

    # Create a list to store routines
    routines = []
    for routine_id, exercises in routine_exercises.items():
        routines.append(
            {
                "id": routine_id,
                "name": routine_map[routine_id],
                "exercises": ", ".join(exercises),
            }
        )

    # Display welcome page
    return render_template("index.html", username=user["username"], routines=routines)


@app.route("/delete/<int:routine_id>")
@login_required
def delete(routine_id):
    """Delete a previously created routine given its ID"""

    # Query database for routine of the user with the given ID
    routine = db.execute(
        "SELECT name FROM routine WHERE id = ? AND user_id = ?",
        routine_id,
        session["user_id"],
    )

    # Ensure routine exists
    if not routine:
        return display_error("Routine not found.")

    # Delete routine from database (since routine_exercise and routine_set have ON
    # DELETE CASCADE, they will be deleted as well)
    db.execute(
        "DELETE FROM routine WHERE id = ? AND user_id = ?",
        routine_id,
        session["user_id"],
    )

    # Redirect user to home page
    return redirect("/")


@app.route("/edit/<int:routine_id>")
@login_required
def edit(routine_id):
    """Edit a previously created routine given its ID"""

    # Get exercises by muscle group
    exercises_by_muscle = fetch_exercises()

    # Get routine data
    routine_name, exercises = fetch_routine(routine_id)

    # Generate times for the rest time dropdown
    times = [{"value": i, "text": format_seconds(i)} for i in range(0, 301, 5)]

    # Display the edit routine page
    return render_template(
        "edit.html",
        routine_id=routine_id,
        routine_name=routine_name,
        exercises=exercises,
        times=times,
        exercises_by_muscle=exercises_by_muscle,
    )


@app.route("/edit", methods=["POST"])
@login_required
def edit_routine():
    """Edit a previously created routine"""

    return display_error("Not implemented yet.")


@app.route("/exercise/<int:exercise_id>")
@login_required
def get_exercise(exercise_id):
    """Get exercise details from the database given its ID"""

    # Query database for exercise with the given ID
    exercise = db.execute(
        """
            SELECT
                exercise.id AS id,
                exercise.name AS name,
                muscle_group.name AS muscle_group
            FROM exercise
            JOIN muscle_group
            ON exercise.muscle_group_id = muscle_group.id
            WHERE exercise.id = ?
        """,
        exercise_id,
    )

    # Ensure exercise exists
    if not exercise:
        return display_error()

    # Return exercise details as JSON
    return jsonify(
        {
            "id": exercise[0]["id"],
            "name": exercise[0]["name"],
            "muscle_group": exercise[0]["muscle_group"],
        }
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Access form username
        username = request.form.get("username")

        # Ensure username was submitted
        if not username:
            return display_error("Must provide username.")

        # Access form password
        password = request.form.get("password")

        # Ensure password was submitted
        if not password:
            return display_error("Must provide password.")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM user WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return display_error("Invalid username and/or password.")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Display log in page
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/new", methods=["GET", "POST"])
@login_required
def new_routine():
    """Create a new routine"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Create routine

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Get exercises by muscle group
        exercises_by_muscle = fetch_exercises()

        # Display new routine page
        return render_template(
            "new.html",
            exercises_by_muscle=exercises_by_muscle,
        )


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Access form username
        username = request.form.get("username")

        # Ensure username was submitted
        if not username:
            return display_error("Missing username.")

        # Access form password
        password = request.form.get("password")

        # Ensure password was submitted
        if not password:
            return display_error("Missing password.")

        # Acces from password confirmation
        confirmation = request.form.get("confirmation")

        # Ensure password confirmation was submitted
        if not confirmation:
            return display_error("Missing password confirmation.")

        # Ensure passwords match
        if password != confirmation:
            return display_error("Passwords don't match.")

        try:
            # Insert user into database
            db.execute(
                "INSERT INTO user (username, hash) VALUES (?, ?)",
                username,
                generate_password_hash(password),
            )
        except ValueError:
            # Render an error if user already exists.
            return display_error("Username already exists.")

        # Redirect user to login form
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Display sign up page
        return render_template("signup.html")


@app.route("/view/<int:routine_id>")
@login_required
def view(routine_id):
    """View a previously created routine given its ID"""

    # Get routine data
    routine_name, exercises = fetch_routine(routine_id)

    # Display the view routine page
    return render_template(
        "view.html",
        routine_id=routine_id,
        routine_name=routine_name,
        exercises=exercises,
    )


def fetch_exercises():
    # Query database for muscle groups
    muscle_groups = db.execute("SELECT * FROM muscle_group")

    # Query database for exercises
    exercises = db.execute("SELECT id, name, muscle_group_id FROM exercise")

    # Map muscle_group IDs to their names
    muscle_group_map = {
        muscle_group["id"]: muscle_group["name"] for muscle_group in muscle_groups
    }

    # Create a dictionary to store exercises by muscle group
    exercises_by_muscle = defaultdict(list)

    # Loop through exercises
    for exercise in exercises:
        # Get the muscle group name
        muscle_group_name = muscle_group_map[exercise["muscle_group_id"]]

        # Add exercise to the dictionary
        exercises_by_muscle[muscle_group_name].append(
            {"id": exercise["id"], "name": exercise["name"]}
        )

    return exercises_by_muscle


def fetch_routine(routine_id):
    """Get routine details given its ID"""

    # Query database for routine of the user with the given ID
    routine = db.execute(
        "SELECT name FROM routine WHERE id = ? AND user_id = ?",
        routine_id,
        session["user_id"],
    )

    # Ensure routine exists
    if not routine:
        return display_error("Routine not found.")

    # Query database for sets of the routine of the user with the given ID
    exercises_flat = db.execute(
        """
            SELECT 
                e.id as exercise_id,
                e.name as exercise_name,
                mg.name as muscle_group,
                re.rest_time,
                rs.weight,
                rs.repetitions
            FROM routine r
            JOIN routine_exercise re ON r.id = re.routine_id
            JOIN exercise e ON re.exercise_id = e.id
            JOIN muscle_group mg ON e.muscle_group_id = mg.id
            JOIN routine_set rs ON re.id = rs.routine_exercise_id
            WHERE r.id = ? AND r.user_id = ?
            ORDER BY re.position, rs.set_number;
        """,
        routine_id,
        session["user_id"],
    )

    # Dictionary to store exercises and sets
    exercises = defaultdict(
        lambda: {"name": "", "muscle_group": "", "rest_time": 0, "sets": []}
    )

    # Loop through each exercise
    for exercise in exercises_flat:
        # Get the exercise ID
        exercise_id = exercise["exercise_id"]

        # Add exercise data to the dictionary
        exercises[exercise_id]["name"] = exercise["exercise_name"]
        exercises[exercise_id]["muscle_group"] = exercise["muscle_group"]
        exercises[exercise_id]["rest_time"] = exercise["rest_time"]
        exercises[exercise_id]["sets"].append(
            {"weight": exercise["weight"], "repetitions": exercise["repetitions"]}
        )

    return routine[0]["name"], exercises
