from flask import url_for, redirect, render_template, request

from application.exceptions import DataValidationError
from application.service import WebAuthService, TokensService
from application.service.users import UsersService
from .forms import ProfileEditForm
from .utils import require_authorized


class ProfileView:
    @staticmethod
    @require_authorized
    def index():
        current_user = WebAuthService.instance().get_authorized_user()
        tokens_service = TokensService.instance()

        return render_template('pages/common/profile.html',
                               page=dict(title='Профиль пользователя', heading='Профиль пользователя'),
                               tokens=tokens_service.get_tokens_by_owner(current_user))

    @staticmethod
    @require_authorized
    def generate_token():
        current_user = WebAuthService.instance().get_authorized_user()
        tokens_service = TokensService.instance()

        tokens_service.create_token(current_user)

        return redirect(url_for('profile'))

    @staticmethod
    @require_authorized
    def delete_token(token_id: int):
        current_user = WebAuthService.instance().get_authorized_user()
        tokens_service = TokensService.instance()

        token = tokens_service.get_token_by_id(token_id)

        if token is not None and token.owner_id == current_user.id:
            tokens_service.delete_token(token)

        return redirect(url_for('profile'))


    @staticmethod
    @require_authorized
    def edit():
        current_user = WebAuthService.instance().get_authorized_user()
        users_service = UsersService.instance()

        form = ProfileEditForm(request.form)

        if request.method == 'GET':
            pass
        elif request.method == 'POST' and form.validate():
            try:
                current_user.password = form.password.data
                users_service.update_user(current_user)

                return redirect(url_for('profile'))
            except DataValidationError as e:
                form.fill_errors(e)

        return render_template('pages/common/profile_edit_form.html',
                               form=form,
                               page=dict(title='Редактирование профиля', heading='Редактирование профиля'))
