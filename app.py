"""Flask app for Feedback"""

from flask import Flask, request, redirect, render_template, flash, jsonify, session
from models import db, connect_db, User, Feedback
from forms import AddUserForm, LoginUserForm, AddFeedbackForm

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

############################################################################################
# Register/Login/Logout
############################################################################################

@app.route("/register", methods=['GET', 'POST'])
def add_user():
    """Add user form"""
    if "user_username" in session:
        return redirect(f"/users/{session['user_username']}")

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
    if "user_username" in session:
        return redirect(f"/users/{session['user_username']}")

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

############################################################################################
# Users
############################################################################################

@app.route("/users/<username>")
def user_details(username):
    """Render user details page"""
    if "user_username" not in session or session["user_username"] != username:
        flash("You must log in to view that page")
        return redirect("/login")

    user = User.query.get_or_404(username)
    return render_template("user.html", user=user)

@app.route("/users/<username>/delete", methods=['POST'])
def delete_user(username):
    """Delete user"""
    if "user_username" not in session or session["user_username"] != username:
        flash("You must log in to delete the user")
        return redirect("/login")
    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("user_username")

    return redirect("/")

############################################################################################
# Feedback
############################################################################################

@app.route("/users/<username>/feedback/add", methods=['GET', 'POST'])
def add_feedback(username):
    """Add feedback form"""
    form = AddFeedbackForm()
    user = User.query.get_or_404(username)

    if "user_username" not in session or session["user_username"] != username:
        flash("You must log in to view that page")
        return redirect("/login")
        
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=user.username)
        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{username}")
    
    return render_template("add-feedback.html", form=form, user=user)

@app.route("/feedback/<feedback_id>/update", methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    """Update feedback form"""
    feedback = Feedback.query.get_or_404(feedback_id)
    form = AddFeedbackForm(obj=feedback)

    if "user_username" not in session or session["user_username"] != feedback.username:
        flash("You must log in to edit that feedback")
        return redirect("/login")

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    return render_template("edit-feedback.html", form=form, feedback=feedback)

@app.route("/feedback/<feedback_id>/delete", methods=['POST'])
def delete_feedback(feedback_id):
    """Delete feedback"""
    feedback = Feedback.query.get_or_404(feedback_id)

    if "user_username" not in session or session["user_username"] != feedback.username:
        flash("You must log in to delete that feedback")
        return redirect("/login")
    db.session.delete(feedback)
    db.session.commit()

    return redirect(f"/users/{feedback.username}")
