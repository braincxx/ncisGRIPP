from application.persistence import UserRole
from application.service.users import UsersService
from application.api.encoder import JSONEncoder
# from application.views.web import *
# from application.views.api import *

from app_instance import server_instance, app, db

db.drop_all()
db.create_all()

if __name__ == '__main__':
    server_instance.add_api('application/api/swagger.yaml', arguments={'title': 'Система онлайн-тестирования'},
                            pythonic_params=True)
    app.json_encoder = JSONEncoder
    app.run()
