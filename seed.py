from app import app
from models import db, User, Feedback


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

f1 = Feedback(
    title="Awesome Product",
    content="These are the best cleats I've ever used. Adidas is the number one brand because it's German!",
    username=u1.username
)

f2 = Feedback(
    title="Lo Mejor",
    content="No lo puedo creer, estas botinas son increibles. Calidad aleman",
    username=u1.username
)
db.session.add_all([u1, u2, f1, f2])
db.session.commit()
