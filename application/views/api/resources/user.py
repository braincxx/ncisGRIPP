from application.api.models import User
from application.api.auth import AuthContext, require_role
from application.exceptions import DataValidationError
from application.persistence import UserRole
from application.service import UsersService

class UserResource:
    @classmethod
    @require_role(role=UserRole.User)
    def get(cls):
        user = AuthContext.instance().authorized_user

        return User.from_persistence(user)
