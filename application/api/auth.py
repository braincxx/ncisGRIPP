from application.persistence import User, UserRole
from application.service import UsersService, TokensService


class AuthContext:
    __instance = None

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = AuthContext()

        return cls.__instance

    def __init__(self):
        super().__init__()

        self._users_service = UsersService.instance()
        self._authorized_user = None

    @property
    def is_authenticated(self):
        return self._authorized_user is not None

    @property
    def authorized_user(self) -> User:
        return self._authorized_user

    def is_access_token_valid(self, token: str):
        return TokensService.instance().get_token_by_value(token) is not None

    def authorize_by_token(self, token: str):
        assert self.is_access_token_valid(token)

        token = TokensService.instance().get_token_by_value(token)
        self._authorized_user = self._users_service.get_user_by_id(token.owner_id)


def require_role(role):
    def require_role_internal_decorator(func):
        def require_role_internal(*args, **kwargs):
            if not AuthContext.instance().is_authenticated and role != UserRole.Guest:
                return 'Unauthorized', 401
            elif AuthContext.instance().is_authenticated and AuthContext.instance().authorized_user.role != role:
                return 'Forbidden', 403

            return func(*args, **kwargs)

        return require_role_internal

    return require_role_internal_decorator
