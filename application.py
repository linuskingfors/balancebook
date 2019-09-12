import os

from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

import json

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
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


@app.route("/")
@login_required
def index():
    """login"""

    return redirect("/new")

@app.route("/data", methods=["GET"])
def data():
    """login"""

    if request.method == "GET":

        # Gets stuff from DB
        data = db.execute("SELECT work, family, hobby, sleep, date FROM library WHERE id = :id ORDER BY date", id=session['user_id'])

        print(data)

        with open("static/chart.json", "w") as f:
            json.dump(data, f)

        # Prepares lists for the data visualisation
        data_work = []
        data_sleep = []
        data_hobby = []
        data_family = []
        data_date = []

        # Goes through the db data and sorts the values into new lists for visualisation
        for d in data:
            data_work.append(d["work"])
            data_family.append(d["family"])
            data_hobby.append(d["hobby"])
            data_sleep.append(d["sleep"])
            data_date.append(d["date"])

        print(data_work)

        return render_template("data.html")
    # If not GET, redirect
    else:
        return redirect("/data")

@app.route("/lib", methods=["GET", "POST"])
@login_required
def lib():
    """login"""

    # Gets stuff from DB
    posts = db.execute("SELECT * FROM library WHERE id = :id ORDER BY date DESC", id=session['user_id'])

    if request.method == "GET":

        # Renders complete page
        return render_template("lib.html", posts=posts)

    if request.method == "POST":

        jinjaid = request.form.get("delete_btn")
        print(jinjaid)
        return apology("things happened")
        # fetch the id of the delete button in question
        # does the
        # delete the post with the ID number of the button

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/new")

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


@app.route("/new", methods=["GET", "POST"])
@login_required
def quote():
    """Create new post."""

    if request.method == 'GET':

        return render_template("new.html")

    if request.method == 'POST':

        # Get "symbol" from the form
        work = int(request.form.get("work"))
        family = int(request.form.get("family"))
        hobby = int(request.form.get("hobby"))
        sleep = int(request.form.get("sleep"))
        thoughts = request.form.get("thoughts")

        if not 0 < work <= 10 or not 0 < family <= 10 or not 0 < hobby <= 10 or not 0 < sleep <= 10:
            return apology("Stop tampering with the form numbers*", 403)

        datecheck = db.execute('SELECT date FROM library WHERE date=:date', date=datetime.today().strftime('%Y-%m-%d'))

        if datecheck:
            return apology("Only one post per day!", 403)

        db.execute('INSERT INTO library (id, work, family, hobby, sleep, thoughts) VALUES (:id, :work, :family, :hobby, :sleep, :thoughts)',
                   id=session['user_id'],
                   work=work,
                   family=family,
                   hobby=hobby,
                   sleep=sleep,
                   thoughts=thoughts)

        return redirect('/lib')

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Loads page for visitors
    if request.method == 'GET':
        return render_template("register.html")

    # Register users
    elif request.method == 'POST':

        password = request.form.get("password")

        # Checks for username
        if not request.form.get("username"):
            return apology("No username, no account", 403)

        # Checks for sync between passwords
        if not password == request.form.get("confirmation"):
            return apology("passwords must match", 403)

        # Checks for number of chars in passwords
        if not len(password) >= 12:
            return apology("More than 12 chars password gaijin", 403)

        # Checks for empty passwords
        if not (request.form.get("password") or request.form.get("confirmation")):
            return apology("Bro, enter a darn password", 403)

        # Checks if username is taken
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # If username exists, break
        if rows:
            return apology("Invalid username", 403)

        # Creates account
        rows = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get(
            "username"), hash=generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8))

        # Loads user account, else returns error
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Log in user
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect('/')


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)