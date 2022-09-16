import os
import requests
import urllib.parse
import webbrowser

from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html", ERROR = "Must Provide Username")
        elif not request.form.get("password"):
            return render_template("error.html", ERROR = "Must Provide Password")
        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("error.html", ERROR = "Password Must Match")
        username = request.form.get("username")
        usernames = db.execute("SELECT username FROM users1")
        if len(usernames) > 0:
            for i in range(len(usernames)):
                if username in usernames[i].get("username"):
                    return render_template("error.html", ERROR = "Username Already Exists")
            password = generate_password_hash(request.form.get("password"))
            db.execute("INSERT INTO users1 (username, hash) VALUES(?, ?)", username, password)
            return redirect("/")
        else:
            password = generate_password_hash(request.form.get("password"))
            db.execute("INSERT INTO users1 (username, hash) VALUES(?, ?)", username, password)
            return redirect("/")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", ERROR = "Must Provide Username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", ERROR = "Must Provide Password")

        # Query database for username
        rows = db.execute("SELECT * FROM users1 WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html", ERROR = "invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/")
@login_required
def apresentation():
    return render_template("apresentation.html")


@app.route("/exercises", methods=["GET", "POST"])
@login_required
def exercises():
    if request.method == "POST":
        if request.form.get("anButton"):
            if not request.form.get("workoutName"):
                return render_template("error.html", ERROR = "Must Provide Exercise Name")
            elif not request.form.get("reps") or "x" not in request.form.get("reps"):
                return render_template("error.html", ERROR = "Must Provide Reps")
            workout = str(request.form.get("workoutName"))
            reps = str(request.form.get("reps"))
            time = datetime.now()
            formatted_time = time.strftime('%Y-%m-%d %H:%M:%S')
            db.execute("INSERT INTO exercises (users_id, repsortimes, exercisesname, type, time) VALUES(?, ?, ?, ?, ?)", session.get("user_id"), reps, workout, "ANAEROBIC", formatted_time)
            return redirect("/done")
        else:
            if not request.form.get("workoutName1"):
                return render_template("error.html", ERROR = "Must Provide Exercise Name")
            elif not request.form.get("time") or "s" not in request.form.get("time"):
                return render_template("error.html", ERROR = "Must Provide Time")
            workout = str(request.form.get("workoutName1"))
            time = str(request.form.get("time"))
            time1 = datetime.now()
            formatted_time = time1.strftime('%Y-%m-%d %H:%M:%S')
            db.execute("INSERT INTO exercises (users_id, repsortimes, exercisesname, type, time) VALUES(?, ?, ?, ?, ?)", session.get("user_id"), time, workout, "AEROBIC", formatted_time)
            return redirect("/done")
    else:
        return render_template("exercises.html")


@app.route("/done")
@login_required
def done():
    exercises = db.execute("SELECT * FROM exercises WHERE users_id = ?", session.get("user_id"))
    username = db.execute("SELECT username FROM users1 WHERE id = ?", session.get("user_id"))
    username = username[0].get("username")
    return render_template("done.html", exercises = exercises, username = username)


@app.route("/change", methods=["GET", "POST"])
@login_required
def changepassword():
    """Change Password"""
    if request.method == "POST":
        if not request.form.get("NEWpassword"):
            return render_template("error.html", ERROR = "Must Provide Password")
        elif request.form.get("NEWpassword") != request.form.get("confirmation"):
            return render_template("error.html", ERROR = "Password Must Match")
        db.execute("UPDATE users1 SET hash = ? WHERE id = ?", generate_password_hash(
            request.form.get("NEWpassword")), session.get("user_id"))
        return redirect("/")
    else:
        return render_template("change.html")


@app.route("/delete", methods=["POST"])
@login_required
def delete():
    """Delete Exercise"""
    exercise = request.form["DeleteButton"]
    db.execute("DELETE FROM exercises WHERE exercisesname = ? AND users_id = ?", exercise, session.get("user_id"))
    return redirect("/done")


@app.route("/search", methods=["POST"])
@login_required
def search():
    exercise = request.form["SearchButton"]
    return redirect(f"https://www.google.com/search?q={exercise}")

