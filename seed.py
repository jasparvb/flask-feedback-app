from app import app
from models import db, User


db.drop_all()
db.create_all()

u1 = User(
    username="messi10",
    password="123456",
    email="messi@fcb.es",
    first_name="Lionel",
    last_name="Messi"
)

u2 = User(
    username="luis9",
    password="123456",
    email="suarez@fcb.es",
    first_name="Luis",
    last_name="Suarez"
)

db.session.add_all([u1, u2])
db.session.commit()