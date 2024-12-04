import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, display_error

# Configure application
app = Flask(__name__)

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
    rows = db.execute("SELECT username FROM user WHERE id = ?", session["user_id"])

    # Display welcome page
    return render_template("index.html", username=rows[0]["username"])


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


@app.route("/routines")
@login_required
def routines():
    """Show user's routines"""

    # Display routines page
    return display_error("Esto aún no está implementado.")


@app.route("/routines/new", methods=["GET", "POST"])
@login_required
def routines_new():
    """Create a new routine"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Redirect user to routines page
        return redirect("/routines")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Display new routine page
        return render_template("routines_new.html")


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
                "INSERT INTO user (username, hash) VALUES(?, ?)",
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
