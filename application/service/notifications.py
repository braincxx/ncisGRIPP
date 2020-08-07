from typing import Optional, List

from application.exceptions import DataValidationError
from application.persistence import User, UserRole, Notification
from application.repository import UsersRepository, NotificationsRepository
from app_instance import bcrypt
from .service import Service
from .validation import DataValidator


class NotificationsService(Service):
    __create_schema = dict(
        title=dict(type='string', required=True, minlength=3, maxlength=120),
        text=dict(type='string', required=True, minlength=3, maxlength=120),
    )

    __update_schema = dict(
        title=dict(type='string', required=True, minlength=3, maxlength=120),
        text=dict(type='string', required=True, minlength=3, maxlength=120),
    )

    __instance = None

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = NotificationsService()

        return cls.__instance

    def __init__(self):
        super().__init__()

        self.notifications_repository = NotificationsRepository.instance()

    def create_user(self, name: str, surname: str, email: str, password: str, role: UserRole):
        data = dict(name=name,
                    surname=surname,
                    email=email,
                    password=password,
                    role=role)

        validation_result, errors = DataValidator.validate_data(data, NotificationsService.__create_schema)

        if not validation_result:
            raise DataValidationError(errors)

        notification = Notification(**data)

        self.notifications_repository.save(notification)

    def update_notification(self, notification: Notification):
        data = dict(title=notification.title,
                    text=notification.text)

        validation_result, errors = DataValidator.validate_data(data,
                                                                NotificationsService.__update_schema)

        if not validation_result:
            raise DataValidationError(errors)

        self.notifications_repository.save(notification)

    def get_by_id(self, notification_id: int):
        return self.notifications_repository.find_by_id(notification_id)

    def get_by_recipient_id(self, recipient_id: int):
        return self.notifications_repository.find_by_recipient_id(recipient_id)

