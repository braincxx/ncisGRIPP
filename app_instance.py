import connexion
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

import config

server_instance = connexion.App(__name__, specification_dir='./')

app = server_instance.app
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{config.SQL_USER}:{config.SQL_PASS}@{config.SQL_HOST}/testing'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
