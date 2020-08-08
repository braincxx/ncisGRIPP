from flask import url_for, redirect
from flask_login import current_user

from application.persistence import UserRole


def require_authorized(func):
    def require_authorization_internal(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))

        return func(*args, **kwargs)

    return require_authorization_internal


def require_role(role):
    def require_role_internal_decorator(func):
        def require_role_internal(*args, **kwargs):
            if not current_user.is_authenticated and role != UserRole.Guest:
                return redirect(url_for('index'))
            elif current_user.is_authenticated and current_user.app_user.role != role:
                return redirect(url_for('index'))

            return func(*args, **kwargs)

        return require_role_internal

    return require_role_internal_decorator
