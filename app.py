import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, love_calculator

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    """Goes to homepage"""
    return render_template("home.html")

@app.route("/compatibility", methods=["GET", "POST"])
@login_required
def compatibility():
    """Shows the compatibility of two people"""

    if request.method == "GET":
        return render_template("compatibility.html")
    
    else:
        # Checks for valid first name
        firstname = request.form.get("firstname")
        if not firstname:
            return apology("must provide name", 400)

        # Checks for valid second name
        secondname = request.form.get("secondname")
        if not secondname:
            return apology("must provide name", 400)

        # Gets the percentage given by the API
        else:
            
            # Cleans the result to only return percentage as an integer in splitpct and quote in splitquote
            answer = love_calculator(firstname, secondname)
            splitpct = int(answer.split('"', 12)[11])
            splitquote = answer.split('"', 16)[15]
            db.execute("INSERT INTO searches (user_id, firstname, secondname, percent) VALUES (?, ?, ?, ?)", session["user_id"], firstname, secondname, splitpct)
            return render_template("percent.html", splitpct=splitpct, splitquote=splitquote, firstname=firstname, secondname=secondname)


@app.route("/history", methods=["GET"])
@login_required
def history():
    """Shows every compatibility search made by user"""

    searches = db.execute("SELECT firstname, secondname, percent FROM searches WHERE user_id = ?", session["user_id"])
    return render_template("history.html", searches=searches)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

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


@app.route("/lovetriangle", methods=["GET", "POST"])
@login_required
def lovetriangle():
    """Shows the most compatible couple in a love triangle"""

    if request.method == "GET":
        return render_template("lovetriangle.html")
    
    else:
        # Checks for valid first name
        firstname = request.form.get("firstname")
        if not firstname:
            return apology("must provide name", 400)

        # Checks for valid second name
        secondname = request.form.get("secondname")
        if not secondname:
            return apology("must provide name", 400)

            # Checks for valid third name
        thirdname = request.form.get("thirdname")
        if not thirdname:
            return apology("must provide name", 400)

        # Gets the percentage given by the API
        else:

            # Gets percent of person one and two
            onetwo = love_calculator(firstname, secondname)
            onetwopct = int(onetwo.split('"', 12)[11])

            # Gets percent of person two and three
            twothree = love_calculator(secondname, thirdname)
            twothreepct = int(twothree.split('"', 12)[11])

            # Gets percent of person one and three
            onethree = love_calculator(firstname, thirdname)
            onethreepct = int(onethree.split('"', 12)[11])

            # Gives the names of the two highest
            if onetwopct > twothreepct and onetwopct > onethreepct:
                couple = "{} and {}".format(firstname, secondname)
                db.execute("INSERT INTO triangle (user_id, firstname, secondname, thirdname, couple) VALUES (?, ?, ?, ?, ?)", session["user_id"], firstname, secondname, thirdname, couple)
                return render_template("solvedtriangle.html", firstname=firstname, secondname=secondname)

            elif twothreepct > onetwopct and twothreepct > onethreepct:
                couple = "{} and {}".format(secondname, thirdname)
                db.execute("INSERT INTO triangle (user_id, firstname, secondname, thirdname, couple) VALUES (?, ?, ?, ?, ?)", session["user_id"], firstname, secondname, thirdname, couple)
                return render_template("solvedtriangle.html", secondname=secondname, thirdname=thirdname)

            elif onethreepct > onetwopct and onethreepct > twothreepct:
                couple = "{} and {}".format(firstname, thirdname)
                db.execute("INSERT INTO triangle (user_id, firstname, secondname, thirdname, couple) VALUES (?, ?, ?, ?, ?)", session["user_id"], firstname, secondname, thirdname, couple)
                return render_template("solvedtriangle.html", firstname=firstname, thirdname=thirdname)

            else:
                couple = "none"
                db.execute("INSERT INTO triangle (user_id, firstname, secondname, thirdname, couple) VALUES (?, ?, ?, ?, ?)", session["user_id"], firstname, secondname, thirdname, couple) 
                return render_template("unsolvable.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template("register.html")

    else:

        # Returns a list of dictionaries with len of num of usernames
        row = db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password and confirmation are the same
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)
        
        # Ensures username is not already taken
        elif len(row) > 0:
            return apology("username taken", 400)

        # Inserts the new user into database
        else:
            username = request.form.get("username")
            hash = generate_password_hash(request.form.get("password"))
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
            return redirect("/")

@app.route("/triangle", methods=["GET"])
@login_required
def triangle():
    """Shows every love triangle search made by user"""

    searches = db.execute("SELECT firstname, secondname, thirdname, couple FROM triangle WHERE user_id = ?", session["user_id"])
    return render_template("triangle.html", searches=searches)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
