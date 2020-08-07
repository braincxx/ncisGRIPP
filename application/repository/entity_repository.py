from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError

from app_instance import db
from application.exceptions.base import AppDataBaseError


def wrap_db_exceptions(func):
    def wrap_db_exceptions_internal(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidRequestError as e:
            raise AppDataBaseError(str(e))
        except SQLAlchemyError as e:
            raise AppDataBaseError(str(e))

    return wrap_db_exceptions_internal


class EntityRepository:
    current_datetime = db.func.now()

    def __init__(self, entity_class):
        self.entity_class = entity_class
