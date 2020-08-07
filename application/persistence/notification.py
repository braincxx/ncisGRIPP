from enum import Enum
from app_instance import db
from . import User


class Level(Enum):
    Advice = 0
    Requirement = 1
    News = 2


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # author_id = db.Column(db.String(80), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(1024), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=db.func.now())

    def __repr__(self):
        return "Notification(id={}, recipient_id={}, title={}, text={}, date={})". \
            format(self.id, self.recipient_id,
                   self.title,
                   self.text, self.date)
