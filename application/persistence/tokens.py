from app_instance import db
from . import User


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime(timezone=True), default=db.func.now())

    def __repr__(self):
        return "Token(id={}, token={}, creation_date={})".format(self.id, self.token, self.creation_date)
