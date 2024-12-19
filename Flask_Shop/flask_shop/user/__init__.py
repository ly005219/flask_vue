from flask import Blueprint
user_bp = Blueprint('user', __name__,url_prefix='/user')

from flask_restful import Api
user_api = Api(user_bp)

from . import views




