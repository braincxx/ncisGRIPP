from flask import url_for, redirect, render_template, request

from application.exceptions import DataValidationError, UserNotFoundError, AppError
from application.hooks import FlaskUser
from application.persistence import UserRole
from application.service import WebAuthService, NotificationsService
from application.service.users import UsersService
from .forms import LoginForm, RegistrationForm, NotificationForm
from .utils import require_authorized, require_role


class TestTasksManagementView:
    @staticmethod
    @require_role(role=UserRole.Teacher)
    def index():
        return render_template('pages/admin/notifications.html',
                               page=dict(title='Управление уведомлениями', heading='Управление уведомлениями'))

    @staticmethod
    @require_role(role=UserRole.Teacher)
    def create():
        form = NotificationForm(request.form)

        if request.method == 'POST' and form.validate():
            try:
                NotificationsService.instance().create(WebAuthService.instance().get_authorized_user(),
                                                             form.name.data, form.description.data,
                                                             form.answer.data,
                                                             form.answer_precision.data)

                return redirect(url_for('test_tasks_manage'))
            except DataValidationError as e:
                form.fill_errors(e)

        return render_template('pages/teacher/test_tasks_form.html',
                               form=form,
                               page=dict(title='Тестовое задание', heading='Тестовое задание'))
