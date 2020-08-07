from flask import render_template
from werkzeug.exceptions import HTTPException
from app_instance import app


# @app.errorhandler(Exception)
# def handle_exception(error):
#     return render_template("errors/generic.html", error=error,
#                            page=dict(title='Непредвиденная ошибка', heading='Непредвиденная ошибка')), 500
