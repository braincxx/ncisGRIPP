from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, TextAreaField, \
    SelectMultipleField, widgets

from application.exceptions import DataValidationError


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ApplicationForm(FlaskForm):
    pass

    def fill_errors(self, validation_error_instance: DataValidationError):
        for field, error in validation_error_instance.errors.items():
            if field in self.__dict__:
                self.__dict__[field].errors.append(error)

    def add_error(self, field, error: str):
        field.errors.append(error)


class LoginForm(ApplicationForm):
    email = StringField('E-mail')
    password = PasswordField('Пароль')


class RegistrationForm(ApplicationForm):
    name = StringField('Имя')
    surname = StringField('Фамилия')
    passport = StringField('Серия и номер паспорта')
    city = StringField('Город')
    street = StringField('Улица')
    email = StringField('E-mail')
    password = PasswordField('Пароль')
    password_confirm = PasswordField('Повторите пароль')
    phone = StringField('Телефон')


class NotificationForm(ApplicationForm):
    title = StringField('Название')
    text = TextAreaField('Текст')


class ProfileEditForm(ApplicationForm):
    city = StringField('Город')
    street = StringField('Улица')

    password = PasswordField('Пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm_password', message='Пароли должны совпадать')
    ])

    confirm_password = PasswordField('Подтверждение пароля')
