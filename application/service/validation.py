from cerberus import Validator
from application.repository import UsersRepository


class DataValidator(Validator):
    DATA_SCHEMA_EMAIL_RULE = dict(type='string', required=True,
                                  regex='^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$')
    DATA_SCHEMA_UNIQUE_EMAIL_RULE = dict(type='string', required=True,
                                         regex='^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$', unique_email=True)

    def _validate_unique_email(self, unique_email, field, value):
        """ Test the uniqueness of an email.
        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        if unique_email and UsersRepository.instance().find_by_email(value) is not None:
            self._error(field, "E-mail must be unique")

    def _validate_such_user_exists_by_id(self, require_user_existence, field, value):
        """ Test the existing of an user.
        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        if require_user_existence and UsersRepository.instance().find_by_id(value) is None:
            self._error(field, "User with such id should exists")

    @staticmethod
    def validate_data(data, schema):
        validator = DataValidator(schema)
        validation_result = validator.validate(data)

        return validation_result, validator.errors
