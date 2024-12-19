from flask import Blueprint

role_bp = Blueprint('role', __name__)

from flask_restful import Api

role_api = Api(role_bp)

from. import views
