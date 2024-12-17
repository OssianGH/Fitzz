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
    login_required,
    muscle_group_image,
)

# Configure application
app = Flask(__name__)

# Custom filters
app.jinja_env.filters["exercise_image"] = exercise_image
app.jinja_env.filters["muscle_group_image"] = muscle_group_image
app.jinja_env.filters["format_add_exercise"] = format_add_exercise

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


@app.route("/exercise/<int:exercise_id>")
@login_required
def get_exercise(exercise_id):
    """Get exercise details from the database given its ID"""

    # Query database for exercise with the given id
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


@app.route("/routine/<int:routine_id>")
@login_required
def get_routine(routine_id):
    """Get routine details from the database given its ID"""

    # Query database for routine of the user with the given id
    routine_name = db.execute(
        "SELECT name FROM routine WHERE id = ? AND user_id = ?",
        routine_id,
        session["user_id"],
    )

    # Ensure routine exists
    if not routine_name:
        return display_error()

    # Query database for exercises and sets of the routine of the user with the given id
    exercises = db.execute(
        """
            SELECT 
                e.id as exercise_id,
                e.name as exercise_name,
                re.rest_time,
                rs.weight,
                rs.repetitions
            FROM routine r
            JOIN routine_exercise re ON r.id = re.routine_id
            JOIN exercise e ON re.exercise_id = e.id
            JOIN routine_set rs ON re.id = rs.routine_exercise_id
            WHERE r.id = ? AND r.user_id = ?
            ORDER BY re.position, rs.set_number;
        """,
        routine_id,
        session["user_id"],
    )

    # Dictionary to store exercises and sets
    exercises_grouped = defaultdict(
        lambda: {"exercise_name": "", "rest_time": 0, "sets": []}
    )

    # Loop through each exercise
    for exercise in exercises:
        # Get the exercise ID
        exercise_id = exercise["exercise_id"]

        # Add exercise data to the dictionary
        exercises_grouped[exercise_id]["exercise_name"] = exercise["exercise_name"]
        exercises_grouped[exercise_id]["rest_time"] = exercise["rest_time"]
        exercises_grouped[exercise_id]["sets"].append(
            {"weight": exercise["weight"], "repetitions": exercise["repetitions"]}
        )

    # Return routine details as JSON
    return jsonify(
        {
            "routine_id": routine_id,
            "routine_name": routine_name[0]["name"],
            "exercises": [
                {
                    "exercise_id": key,
                    "exercise_name": value["exercise_name"],
                    "rest_time": value["rest_time"],
                    "sets": value["sets"],
                }
                for key, value in exercises_grouped.items()
            ],
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


@app.route("/routine/new", methods=["GET", "POST"])
@login_required
def routine_new():
    """Create a new routine"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Access form routine name
        routine_name = request.form.get("routine-name")

        # Ensure routine name was submitted
        if not routine_name:
            return display_error("Routine name must be filled.")

        # Access form exercise count
        exercise_count = request.form.get("exercise-count")

        # Ensure exercise count was submitted
        if not exercise_count:
            return display_error()

        # Ensure exercise count is integer
        try:
            exercise_count = int(exercise_count)
        except:
            return display_error()

        # Ensure the routine has at least one exercise
        if exercise_count < 1:
            return display_error("There must be at least one exercise in the routine.")

        # Dictionary to store exercises and sets
        exercises_data = {}

        # Loop through each exercise
        for exercise_number in range(1, exercise_count + 1):
            # Access form current exercise id
            exercise_id = request.form.get(f"exercise-{exercise_number}-id")

            # Ensure current exercise id was submitted
            if not exercise_id:
                return display_error()

            # Access form current exercise set count
            exercise_set_count = request.form.get(
                f"exercise-{exercise_number}-set-count"
            )

            # Ensure current exercise set count was submitted
            if not exercise_set_count:
                return display_error()

            # Ensure current exercise set count is integer
            try:
                exercise_set_count = int(exercise_set_count)
            except:
                return display_error()

            # Ensure the current exercise has at least one set
            if exercise_set_count < 1:
                return display_error(
                    f"Exercise {exercise_number} must have at least one set."
                )

            # Access form current exercise rest time
            exercise_rest = request.form.get(f"exercise-{exercise_number}-rest")

            # Ensure current exercise rest time was submitted
            if not exercise_rest:
                exercise_rest = 0
            else:
                # Ensure current exercise rest time is integer
                try:
                    exercise_rest = int(exercise_rest)
                except:
                    return display_error(
                        f"Exercise {exercise_number} rest time must be an integer"
                    )

            # Ensure current exercise rest time is positive
            if exercise_rest < 0:
                return display_error(
                    f"Exercise {exercise_number} rest time must be positive."
                )

            # Ensure current exercise rest time is less than 300 seconds
            if exercise_rest > 300:
                return display_error(
                    f"Exercise {exercise_number} rest time is too long."
                )

            # Ensure current exercise rest time is multiple of 5
            if exercise_rest % 5 != 0:
                return display_error(
                    f"Exercise {exercise_number} rest time is invalid."
                )

            # List to store sets of the current exercise
            exercise_sets = []

            # Loop through each set of the current exercise
            for set_number in range(1, exercise_set_count + 1):
                # Access form current set weight
                weight = request.form.get(
                    f"exercise-{exercise_number}-set-{set_number}-weight"
                )

                # Ensure current set weight was submitted
                if not weight:
                    return display_error(
                        f"Missing exercise {exercise_number} set {set_number} weight."
                    )

                # Ensure current set weight is integer
                try:
                    weight = int(weight)
                except:
                    return display_error(
                        f"Exercise {exercise_number} set {set_number} weight must be an integer."
                    )

                # Ensure current set weight is positive
                if weight < 1:
                    return display_error(
                        f"Exercise {exercise_number} set {set_number} weight must be positive."
                    )

                # Access form current set reps
                reps = request.form.get(
                    f"exercise-{exercise_number}-set-{set_number}-reps"
                )

                # Ensure current set reps was submitted
                if not reps:
                    return display_error(
                        f"Missing exercise {exercise_number} set {set_number} reps."
                    )

                # Ensure current set reps is integer
                try:
                    reps = int(reps)
                except:
                    return display_error(
                        f"Exercise {exercise_number} set {set_number} reps must be an integer."
                    )

                # Ensure current set reps is positive
                if reps < 1:
                    return display_error(
                        f"Exercise {exercise_number} set {set_number} reps must be positive."
                    )

                # Add set data to the list
                exercise_sets.append({"weight": weight, "reps": reps})

            # Store the sets under the exercise ID
            exercises_data[exercise_id] = {
                "rest_time": exercise_rest,
                "sets": exercise_sets,
            }

        # Create database entries
        routine_id = db.execute(
            "INSERT INTO routine (user_id, name) VALUES (?, ?)",
            session["user_id"],
            routine_name.strip(),
        )

        for position, (exercise_id, exercise) in enumerate(
            exercises_data.items(), start=1
        ):
            routine_exercise_id = db.execute(
                "INSERT INTO routine_exercise (routine_id, exercise_id, position, rest_time) VALUES (?, ?, ?, ?)",
                routine_id,
                exercise_id,
                position,
                exercise["rest_time"],
            )
            for set_number, routine_set in enumerate(exercise["sets"], start=1):
                db.execute(
                    "INSERT INTO routine_set (routine_exercise_id, set_number, weight, repetitions) VALUES (?, ?, ?, ?)",
                    routine_exercise_id,
                    set_number,
                    routine_set["weight"],
                    routine_set["reps"],
                )

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
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

        # Display new routine page
        return render_template(
            "routines_new.html",
            exercises_by_muscle=exercises_by_muscle,
        )


@app.route("/routine/view", methods=["POST"])
@login_required
def routine_view():
    """View routine exercises and sets"""

    return "Por implementar"


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
