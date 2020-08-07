from application.persistence import Token
from application.repository.entity_repository import EntityRepository, wrap_db_exceptions
from app_instance import db


class TokensRepository(EntityRepository):
    __instance = None

    def __init__(self):
        super().__init__(Token)

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = TokensRepository()

        return cls.__instance

    @wrap_db_exceptions
    def save(self, token: Token):
        if token.id is None:
            db.session.add(token)

        db.session.commit()

    @wrap_db_exceptions
    def delete(self, token: Token):
        db.session.delete(token)
        db.session.commit()

    @wrap_db_exceptions
    def find_by_id(self, id: int) -> Token:
        return Token.query.filter_by(id=int(id)).first()

    @wrap_db_exceptions
    def find_by_owner_id(self, owner_id: int) -> Token:
        return Token.query.filter_by(owner_id=int(owner_id)).all()

    @wrap_db_exceptions
    def find_by_token(self, token: str) -> Token:
        return Token.query.filter_by(token=str(token)).first()

    @wrap_db_exceptions
    def get_all(self):
        return Token.query.all()

    @wrap_db_exceptions
    def count_all(self) -> int:
        return len(Token.query.all())
