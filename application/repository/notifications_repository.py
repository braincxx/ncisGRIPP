from application.persistence import Notification
from application.repository.entity_repository import EntityRepository, wrap_db_exceptions
from app_instance import db


class NotificationsRepository(EntityRepository):
    __instance = None

    def __init__(self):
        super().__init__(Notification)

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = NotificationsRepository()

        return cls.__instance

    @wrap_db_exceptions
    def save(self, notification: Notification):
        if notification.id is None:
            db.session.add(notification)

        db.session.commit()

    @wrap_db_exceptions
    def delete(self, notification: Notification):
        db.session.delete(notification)
        db.session.commit()

    @wrap_db_exceptions
    def find_by_id(self, id: int) -> Notification:
        return Notification.query.filter_by(id=int(id)).first()

    @wrap_db_exceptions
    def find_by_recipient_id(self, recipient_id: int) -> Notification:
        return Notification.query.filter_by(recipient_id=int(recipient_id)).all()

    @wrap_db_exceptions
    def find_by_email(self, email: str) -> Notification:
        return Notification.query.filter_by(email=str(email)).first()

    @wrap_db_exceptions
    def get_all(self) -> Notification:
        return Notification.query.all()
