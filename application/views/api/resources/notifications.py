from application.api.models import User, Notification
from application.api.auth import AuthContext, require_role
from application.exceptions import DataValidationError
from application.persistence import UserRole
from application.service import UsersService, NotificationsService


class NotificationsResource:
    @classmethod
    @require_role(role=UserRole.User)
    def get(cls):
        user = AuthContext.instance().authorized_user
        notifications = NotificationsService.instance().get_by_recipient_id(user.id)

        return [Notification.from_persistence(notification) for notification in notifications]
