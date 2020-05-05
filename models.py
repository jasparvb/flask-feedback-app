"""Models for Feedback app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS GO BELOW!
class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)

    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.String(50), nullable=False)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)
  
    def __repr__(self):
        u = self
        return f"<User username={u.username} first_name={u.first_name} last_name={u.last_name}>"
