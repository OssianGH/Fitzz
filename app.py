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

    # Remove routine from database
    try:
        remove_routine(routine_id)
    except ValueError as e:
        return display_error(str(e))

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
def edit_post():
    """Validate and make the modifications to the routine"""

    # Access form routine ID
    routine_id = request.form.get("routine-id")

    # Ensure routine ID was submitted
    if not routine_id:
        return display_error()

    # Remove routine from database
    try:
        remove_routine(routine_id)
    except ValueError as e:
        return display_error(str(e))

    # Create routine
    try:
        create_routine()
    except ValueError as e:
        return display_error(str(e))
    except SystemError:
        return display_error()

    # Redirect user to home page
    return redirect("/")


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
        try:
            create_routine()
        except ValueError as e:
            return display_error(str(e))
        except SystemError:
            return display_error()

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


def create_routine():
    # Access form routine name
    routine_name = request.form.get("routine-name")

    # Ensure routine name was submitted
    if not routine_name:
        raise ValueError("Routine name must be filled.")

    # Access form exercise count
    exercise_count = request.form.get("exercise-count")

    # Ensure exercise count was submitted
    if not exercise_count:
        raise SystemError()

    # Ensure exercise count is integer
    try:
        exercise_count = int(exercise_count)
    except:
        raise SystemError()

    # Ensure the routine has at least one exercise
    if exercise_count < 1:
        raise ValueError("There must be at least one exercise in the routine.")

    # Dictionary to store exercises and sets
    exercises_data = {}

    # Loop through each exercise
    for exercise_number in range(1, exercise_count + 1):
        # Access form current exercise ID
        exercise_id = request.form.get(f"exercise-{exercise_number}-id")

        # Ensure current exercise ID was submitted
        if not exercise_id:
            raise SystemError()

        # Access form current exercise set count
        exercise_set_count = request.form.get(f"exercise-{exercise_number}-set-count")

        # Ensure current exercise set count was submitted
        if not exercise_set_count:
            raise SystemError()

        # Ensure current exercise set count is integer
        try:
            exercise_set_count = int(exercise_set_count)
        except:
            raise SystemError()

        # Ensure the current exercise has at least one set
        if exercise_set_count < 1:
            raise ValueError(f"Exercise {exercise_number} must have at least one set.")

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
                raise ValueError(
                    f"Exercise {exercise_number} rest time must be an integer"
                )

        # Ensure current exercise rest time is positive
        if exercise_rest < 0:
            raise ValueError(f"Exercise {exercise_number} rest time must be positive.")

        # Ensure current exercise rest time is less than 300 seconds
        if exercise_rest > 300:
            raise ValueError(f"Exercise {exercise_number} rest time is too long.")

        # Ensure current exercise rest time is multiple of 5
        if exercise_rest % 5 != 0:
            raise ValueError(f"Exercise {exercise_number} rest time is invalid.")

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
                raise ValueError(
                    f"Missing exercise {exercise_number} set {set_number} weight."
                )

            # Ensure current set weight is integer
            try:
                weight = int(weight)
            except:
                raise ValueError(
                    f"Exercise {exercise_number} set {set_number} weight must be an integer."
                )

            # Ensure current set weight is positive
            if weight < 1:
                raise ValueError(
                    f"Exercise {exercise_number} set {set_number} weight must be positive."
                )

            # Access form current set reps
            reps = request.form.get(f"exercise-{exercise_number}-set-{set_number}-reps")

            # Ensure current set reps was submitted
            if not reps:
                raise ValueError(
                    f"Missing exercise {exercise_number} set {set_number} reps."
                )

            # Ensure current set reps is integer
            try:
                reps = int(reps)
            except:
                raise ValueError(
                    f"Exercise {exercise_number} set {set_number} reps must be an integer."
                )

            # Ensure current set reps is positive
            if reps < 1:
                raise ValueError(
                    f"Exercise {exercise_number} set {set_number} reps must be positive."
                )

            # Add set data to the list
            exercise_sets.append({"weight": weight, "reps": reps})

        # Store the sets under the exercise ID
        exercises_data[exercise_id] = {
            "rest_time": exercise_rest,
            "sets": exercise_sets,
        }

    # Insert routine into database
    routine_id = db.execute(
        "INSERT INTO routine (user_id, name) VALUES (?, ?)",
        session["user_id"],
        routine_name.strip(),
    )

    # Insert exercises of the routine into database
    for position, (exercise_id, exercise) in enumerate(exercises_data.items(), start=1):
        routine_exercise_id = db.execute(
            "INSERT INTO routine_exercise (routine_id, exercise_id, position, rest_time) VALUES (?, ?, ?, ?)",
            routine_id,
            exercise_id,
            position,
            exercise["rest_time"],
        )
        # Insert sets of the current exercise into database
        for set_number, routine_set in enumerate(exercise["sets"], start=1):
            db.execute(
                "INSERT INTO routine_set (routine_exercise_id, set_number, weight, repetitions) VALUES (?, ?, ?, ?)",
                routine_exercise_id,
                set_number,
                routine_set["weight"],
                routine_set["reps"],
            )


def remove_routine(routine_id):
    # Query database for routine of the user with the given ID
    routine = db.execute(
        "SELECT name FROM routine WHERE id = ? AND user_id = ?",
        routine_id,
        session["user_id"],
    )

    # Ensure routine exists
    if not routine:
        raise ValueError("Routine not found.")

    # Delete routine from database (since routine_exercise and routine_set have ON
    # DELETE CASCADE, they will be deleted as well)
    db.execute(
        "DELETE FROM routine WHERE id = ? AND user_id = ?",
        routine_id,
        session["user_id"],
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
