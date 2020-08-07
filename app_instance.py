import connexion
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

server_instance = connexion.App(__name__, specification_dir='./')

app = server_instance.app
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://test:qwerty@127.0.0.1/testing'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
