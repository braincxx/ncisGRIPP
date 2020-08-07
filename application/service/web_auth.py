from typing import Optional
from application.exceptions import UserNotFoundError, DataValidationError, BadAccessError
from application.persistence import User, UserRole
from application.hooks import FlaskUser
from application.service.validation import DataValidator
from .service import Service
from .users import UsersService


class WebAuthService(Service):
    __authorize_user_schema = dict(
        email=DataValidator.DATA_SCHEMA_EMAIL_RULE,
        password=dict(type='string', required=True, minlength=3, maxlength=60),
    )

    __instance = None

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = WebAuthService()

        return cls.__instance

    def __init__(self):
        super().__init__()

        self.users_service = UsersService.instance()

    def get_authorized_user(self) -> Optional[User]:
        user = FlaskUser.get_current_user_or_null()

        if user is not None:
            return user.app_user

        return None

    def get_current_user_role(self) -> UserRole:
        return FlaskUser.get_current_user_role()

    def is_authorized(self) -> bool:
        return self.get_current_user_role() != UserRole.Guest

    def authorize(self, email: str, password: str):
        validation_result, errors = DataValidator.validate_data(dict(email=email, password=password),
                                                                WebAuthService.__authorize_user_schema)

        if not validation_result:
            raise DataValidationError(errors)

        user = self.users_service.find_user_by_credentials(email, password)

        if not user:
            raise UserNotFoundError

        FlaskUser.authorize(user)

    def logout(self):
        if not self.is_authorized():
            raise BadAccessError

        FlaskUser.logout()
