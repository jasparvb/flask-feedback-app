"""Flask app for Feedback"""

from flask import Flask, request, redirect, render_template, flash, jsonify
from models import db, connect_db, User
from forms import AddUserForm

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

@app.route("/register", methods=['GET', 'POST'])
def add_user():
    """Add user form"""
    form = AddUserForm()
    return render_template("register.html", form=form)

