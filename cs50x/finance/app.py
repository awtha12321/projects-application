import os
import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    recent_row = db.execute("SELECT name, symbol, price, SUM(shares) AS share, SUM(total) AS total, buy, sell FROM history WHERE username_id = ? GROUP BY symbol", session["user_id"])

    buy_total = 0
    sell_total = 0

    # print(recent_row)
    for i in range(len(recent_row)):
        if recent_row[i]["buy"] == 1:
            buy_total += recent_row[i]["total"]
        elif recent_row[i]["sell"] == 1:
            sell_total += recent_row[i]["total"]

    row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    cur_cash = row[0]["cash"]

    total_amount = (cur_cash + buy_total) - sell_total

    return render_template("index.html", recent_row=recent_row, cur_cash=cur_cash, total_amount=total_amount)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        stock = request.form.get("symbol")

        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("shares must be a posative integer", 400)

        if not stock:
            return apology("must provide Symbol", 400)

        if not shares:
            return apology("must provide shares", 400)

        if shares is float:
            return apology("must provide integer", 400)

        if shares < 0:
            return apology("must provide positive numbers", 400)


        stock2 = lookup(stock)

        if not stock2:
            return apology("symbol does not exist", 400)

        name = stock2["name"]
        price = stock2["price"]
        symbol = stock2["symbol"]
        total = 0

        rows = db.execute("SELECT * FROM users WHERE id = ? ", session["user_id"])
        cur_cash = rows[0]["cash"]

        time =  datetime.datetime.now()

        for i in range(shares):
            total += price

        if cur_cash < total:
            return apology("You do not have enough money to buy", 400)

        cur_cash -= total

        insert = "INSERT INTO history (username_id, name, shares, price, symbol, total, time, buy, sell) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

        db.execute(insert, session["user_id"], name, shares, price, symbol, total, time, True, False)

        db.execute("UPDATE users SET cash = ? WHERE id = ?",  cur_cash, session["user_id"])

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    recent_row = db.execute("SELECT * FROM history WHERE username_id = ?", session["user_id"])

    return render_template("history.html", recent_row=recent_row)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # print(session["user_id"])

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol", 400)

        result = lookup(symbol)

        if not result:
            return apology("Symbol does not exist", 400)

        amount = result["price"]

        amount2 = usd(amount)

        return render_template("quoted.html", result=result, amount2=amount2)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("confirmation")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if not username:
            return apology("must provide username", 400)

        if not password:
            return apology("must provide password", 400)

        if not password2:
            return apology("must provide password again", 400)

        if password != password2:
            return apology("passwords do not match", 400)

        if len(rows) != 1:
            insert = "INSERT INTO users (username, hash) VALUES (?, ?)"
            u = username
            pwhash = generate_password_hash(password,  method='pbkdf2:sha256', salt_length=8)
            db.execute(insert, u, pwhash)
        else:
            return apology("Username already exists")

        return render_template("login.html")

    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    symbol_ = db.execute("SELECT symbol FROM history WHERE username_id = ? GROUP BY symbol", session["user_id"])

    if request.method == "POST":
        sell_symbol = request.form.get("symbol")

        try:
            share = int(request.form.get("shares"))
        except ValueError:
            return apology("shares must be a posative integer", 400)

        if not sell_symbol:
            return apology("must provide Symbol", 400)

        if not share:
            return apology("must provide Shares", 400)

        if share is float:
            return apology("must provide integer", 400)

        if share < 0:
            return apology("must provide positive number", 400)

        sell_share = -abs(share)

        stock = lookup(sell_symbol)

        if not stock:
            return apology("symbol does not exist", 400)

        name = stock["name"]
        price = stock["price"]
        symbol = stock["symbol"]
        total = 0

        symbol_f_db = db.execute("SELECT SUM(shares) AS shares, symbol FROM history WHERE username_id = ? GROUP BY symbol", session["user_id"])

        length = len(symbol_f_db)

        symbols = []

        for y in range(length):
            symbols.append(symbol_f_db[y]["symbol"])
        # print(symbols)

        if sell_symbol in symbols:
            for r in range(length):
                if symbol_f_db[r]["symbol"] == sell_symbol:
                    if share > symbol_f_db[r]["shares"]:
                        return apology("You do not have enough stock.", 400)
        else:
            return apology("You do not have the stock.", 400)

        rows = db.execute("SELECT * FROM users WHERE id = ? ", session["user_id"])
        cur_cash = rows[0]["cash"]

        time =  datetime.datetime.now()

        for i in range(share):
            total += price

        cur_cash += total

        insert = "INSERT INTO history (username_id, name, shares, price, symbol, total, time, buy, sell) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

        db.execute(insert, session["user_id"], name, sell_share, price, symbol, total, time, False, True)

        db.execute("UPDATE users SET cash = ? WHERE id = ?",  cur_cash, session["user_id"])

        return redirect("/")

    else:
        return render_template("sell.html", symbol_=symbol_)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
