from application.persistence import User, UserRole
from application.repository.entity_repository import EntityRepository, wrap_db_exceptions
from app_instance import db


class UsersRepository(EntityRepository):
    __instance = None

    def __init__(self):
        super().__init__(User)

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = UsersRepository()

        return cls.__instance

    @wrap_db_exceptions
    def save(self, user: User):
        if user.id is None:
            db.session.add(user)

        db.session.commit()

    @wrap_db_exceptions
    def delete(self, user: User):
        db.session.delete(user)
        db.session.commit()

    @wrap_db_exceptions
    def find_by_id(self, id: int) -> User:
        return User.query.filter_by(id=int(id)).first()

    @wrap_db_exceptions
    def find_by_email(self, email: str) -> User:
        return User.query.filter_by(email=str(email)).first()

    @wrap_db_exceptions
    def get_all(self) -> User:
        return User.query.all()

    @wrap_db_exceptions
    def get_by_role(self, role: UserRole):
        return User.query.filter_by(role=role).all()
