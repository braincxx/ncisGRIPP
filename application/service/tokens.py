import secrets
from typing import Optional, List

from application.exceptions import DataValidationError
from application.exceptions.users import UserAlreadyExistsError
from application.persistence import User, UserRole, Token
from application.repository import UsersRepository, TokensRepository
from app_instance import bcrypt
from .service import Service
from .validation import DataValidator


class TokensService(Service):
    TOKEN_LENGTH = 24

    __instance = None

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = TokensService()

        return cls.__instance

    def __init__(self):
        super().__init__()

        self.tokens_repository = TokensRepository.instance()

    def get_token_by_id(self, token_id: int) -> Token:
        return self.tokens_repository.find_by_id(token_id)

    def get_token_by_value(self, token: str) -> Token:
        return self.tokens_repository.find_by_token(token)

    def get_tokens_by_owner(self, owner: User) -> List[Token]:
        return self.tokens_repository.find_by_owner_id(owner.id)

    def create_token(self, owner: User):
        token = Token(owner_id=owner.id, token=self._generate_token())
        self.tokens_repository.save(token)

    def delete_token(self, token: Token):
        self.tokens_repository.delete(token)

    def _generate_token(self):
        return secrets.token_hex(TokensService.TOKEN_LENGTH)
