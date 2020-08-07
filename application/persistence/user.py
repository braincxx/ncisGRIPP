from enum import Enum
from app_instance import db


class UserRole(Enum):
    Guest = 0
    User = 1
    Admin = 2


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    passport = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    city = db.Column(db.String(120), unique=True, nullable=False)
    street = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    registration_date = db.Column(db.DateTime(timezone=True), default=db.func.now())

    received_notifications = db.relationship('Notification', cascade="all, delete-orphan")
    created_tokens = db.relationship('Token', backref='owner', cascade="all, delete-orphan")

    def __repr__(self):
        return "User(id={}, name={}, surname={}, email={}, role={})".format(self.id, self.name, self.surname,
                                                                            self.email, self.role)
