import connexion
import six

from application.api import util
from application.api.models import Error, User, Notification
from application.api.auth import AuthContext
from .resources.user import UserResource
from .resources.notifications import NotificationsResource
from .utils import handle_bad_requests
from ...exceptions.requests import PageNotFoundError


def check_ApiKeyAuth(api_key, required_scopes):
    if not AuthContext.instance().is_access_token_valid(api_key):
        return None

    AuthContext.instance().authorize_by_token(api_key)
    return dict(authorized=True)


@handle_bad_requests
def notifications_get(**kwargs):
    return NotificationsResource.get()


@handle_bad_requests
def users_user_id_get(user_id: int, **kwargs):
    return UserResource.get(int(user_id))

