from flask_login import UserMixin, login_user, logout_user, current_user

from application.exceptions import BadAccessError
from application.persistence import User, UserRole
from app_instance import login_manager
from application.repository import UsersRepository


class FlaskUser(UserMixin):
    def __init__(self, user: User):
        self.id = user.id
        self.app_user = user

    def __repr__(self):
        return "FlaskUser(id={}, app_user={})".format(self.id, self.app_user)

    @staticmethod
    def authorize(user: User):
        login_user(FlaskUser(user))

    @staticmethod
    def logout():
        logout_user()

    @staticmethod
    def get_current_user_or_null():
        user = current_user

        if user.is_anonymous or not user.is_authenticated:
            return None

        return user

    @staticmethod
    def get_current_user_role() -> UserRole:
        authorized_user = FlaskUser.get_current_user_or_null()

        if authorized_user is None:
            return UserRole.Guest

        return authorized_user.app_user.role


@login_manager.user_loader
def load_user(user_id):
    return FlaskUser(UsersRepository.instance().find_by_id(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    print('Access denied')



