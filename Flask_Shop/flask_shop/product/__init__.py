from flask import Blueprint
from flask_restful import Api


product_bp = Blueprint('product', __name__)
product_api = Api(product_bp)

from . import views