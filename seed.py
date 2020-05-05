from app import app
from models import db, User


db.drop_all()
db.create_all()

u1 = User.register(
    "messi10",
    "123456",
    "messi@fcb.es",
    "Lionel",
    "Messi"
)

u2 = User.register(
    "luis9",
    "123456",
    "suarez@fcb.es",
    "Luis",
    "Suarez"
)

db.session.add_all([u1, u2])
db.session.commit()