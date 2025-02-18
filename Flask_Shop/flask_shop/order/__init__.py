from flask import Blueprint
from flask_restful import Api


order_bp = Blueprint('order', __name__)
order_api = Api(order_bp)
from. import views

