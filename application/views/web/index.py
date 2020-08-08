from flask import url_for, redirect, render_template, request

from application.exceptions import DataValidationError, UserNotFoundError, AppError
from application.hooks import FlaskUser
from application.hooks.template_context_processing import format_datetime
from application.persistence import UserRole
from application.service import WebAuthService, NotificationsService
from application.service.users import UsersService
from .forms import LoginForm, RegistrationForm
from .utils import require_authorized, require_role


class IndexView:
    @staticmethod
    def index():
        return render_template('pages/common/index.html', page=dict(title='Главная', heading='Главная'))

        # if WebAuthService.instance().get_current_user_role() == UserRole.User:
        #     return redirect(url_for('user_dashboard'))
        # elif WebAuthService.instance().get_current_user_role() == UserRole.Admin:
        #     return redirect(url_for('admin_dashboard'))
        # else:
        #     raise NotImplementedError

    @staticmethod
    def map():
        return render_template('pages/common/virus_map.html', page=dict(title='Карта очагов заболеваемости', heading='Карта очагов заболеваемости'))

    @staticmethod
    def actions():
        return render_template('pages/common/news.html', page=dict(title='Меры', heading='Меры'))

    @staticmethod
    def news():
        return render_template('pages/common/actions.html', page=dict(title='Новости', heading='Новости'))

    @staticmethod
    def about():
        return render_template('pages/common/about.html', page=dict(title='О команде', heading='О команде'))

    @staticmethod
    @require_role(role=UserRole.Guest)
    def login():
        form = LoginForm(request.form)

        if request.method == 'POST' and form.validate():
            try:
                WebAuthService.instance().authorize(form.email.data, form.password.data)

                return redirect(url_for('dashboard'))
            except DataValidationError as e:
                form.fill_errors(e)
            except UserNotFoundError as e:
                form.add_error(form.email, 'Пользователя с такими данными не существует')

        return render_template('pages/login.html', form=form, page=dict(title='Авторизация', heading='Авторизация'))

    @staticmethod
    @require_role(role=UserRole.Guest)
    def register():
        form = RegistrationForm(request.form)

        if request.method == 'POST' and form.validate():
            try:
                if form.password.data != form.password_confirm.data:
                    raise DataValidationError(dict(password='Пароли не совпадают'))

                UsersService.instance().create_user(form.name.data, form.surname.data, form.email.data,
                                                    form.password.data,
                                                    form.city.data, form.street.data,
                                                    form.phone.data,
                                                    form.passport.data,
                                                    UserRole(UserRole.User))

                WebAuthService.instance().authorize(form.email.data, form.password.data)

                return redirect(url_for('dashboard'))
            except DataValidationError as e:
                form.fill_errors(e)
            except UserNotFoundError as e:
                form.add_error(form.email, 'Пользователя с такими данными не существует')

        return render_template('pages/login.html', form=form,
                               page=dict(title='Авторизация', heading='Авторизация'))

    @staticmethod
    @require_authorized
    def logout():
        WebAuthService.instance().logout()
        return redirect(url_for('index'))

    @staticmethod
    @require_authorized
    def dashboard():
        current_user = WebAuthService.instance().get_authorized_user()

        if current_user.role == UserRole.User:
            notifications = NotificationsService.instance().get_by_recipient_id(current_user.id)

            return render_template('pages/user/user_dashboard.html',
                                   page=dict(title='Панель пользователя', heading='Панель пользователя'), notifications=notifications)
        else:
            return render_template('pages/admin/admin_dashboard.html',
                                   page=dict(title='Панель администратора', heading='Панель администратора'))
