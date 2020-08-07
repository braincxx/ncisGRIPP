from typing import Optional, List

from application.exceptions import DataValidationError
from application.exceptions.users import UserAlreadyExistsError
from application.persistence import User, UserRole
from application.repository import UsersRepository
from app_instance import bcrypt
from .service import Service
from .validation import DataValidator


class UsersService(Service):
    __create_user_schema = dict(
        name=dict(type='string', required=True, minlength=3, maxlength=60),
        surname=dict(type='string', required=True, minlength=3, maxlength=60),
        email=DataValidator.DATA_SCHEMA_UNIQUE_EMAIL_RULE,
        password=dict(type='string', required=True, minlength=3, maxlength=60),
        role=dict(allowed=[UserRole.Admin, UserRole.User])
    )

    __update_user_schema = dict(
        name=dict(type='string', required=True, minlength=3, maxlength=60),
        surname=dict(type='string', required=True, minlength=3, maxlength=60),
        password=dict(type='string', required=True, minlength=3, maxlength=60),
    )

    __instance = None

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = UsersService()

        return cls.__instance

    def __init__(self):
        super().__init__()

        self.users_repository = UsersRepository.instance()

    def create_user(self, name: str, surname: str, email: str, password: str, role: UserRole):
        user_data = dict(name=name,
                         surname=surname,
                         email=email,
                         password=password,
                         role=role)

        validation_result, errors = DataValidator.validate_data(user_data, UsersService.__create_user_schema)

        if not validation_result:
            raise DataValidationError(errors)

        user_data['password'] = self.__hash_password(user_data['password'])

        user = User(**user_data)

        self.users_repository.save(user)

    def update_user(self, user: User):
        user_data = dict(name=user.name,
                         surname=user.surname,
                         password=user.password)

        validation_result, errors = DataValidator.validate_data(user_data,
                                                                UsersService.__update_user_schema)

        if not validation_result:
            raise DataValidationError(errors)

        user.password = self.__hash_password(user.password)

        self.users_repository.save(user)

    def find_user_by_credentials(self, email: str, password: str) -> Optional[User]:
        user = self.users_repository.find_by_email(email)

        if user is None:
            return None

        if not self.__check_password_hash(password, user.password):
            return None

        return user

    def get_user_by_id(self, user_id: int):
        return self.users_repository.find_by_id(user_id)

    def get_by_role(self, role: UserRole) -> List[User]:
        return self.users_repository.get_by_role(role)

    def __hash_password(self, password):
        return bcrypt.generate_password_hash(password).decode()

    def __check_password_hash(self, password, password_hash):
        return bcrypt.check_password_hash(password_hash, password)
