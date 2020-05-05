"""Flask app for Feedback"""

from flask import Flask, request, redirect, render_template, flash, jsonify, session
from models import db, connect_db, User
from forms import AddUserForm, LoginUserForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:41361@localhost/feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route("/")
def home():
    """Redirect to add user form"""
    return redirect("/register")

@app.route("/users/<username>")
def user_details(username):
    """Render user details page"""
    if "user_username" not in session:
        flash("You must log in to view that page")
        return redirect("/login")

    user = User.query.get_or_404(username)
    return render_template("user.html", user=user)

@app.route("/register", methods=['GET', 'POST'])
def add_user():
    """Add user form"""
    form = AddUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        db.session.commit()

        return redirect(f"/users/{username}")
    
    return render_template("register.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_user():
    """Login user form"""
    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.login(username, password)
        if user:
            session["user_username"] = user.username
            return redirect(f"/users/{username}")
        else:
            form.username.errors = ["Bad username/password"]

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("user_username")

    return redirect("/")