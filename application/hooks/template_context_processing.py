from app_instance import app
from application.persistence import UserRole


@app.context_processor
def inject_user_role():
    return dict(UserRole=UserRole)


@app.template_filter('format_date_time')
def format_datetime(value, format="%d.%m.%Y"):
    if value is None:
        return ""
    return value.strftime(format)
