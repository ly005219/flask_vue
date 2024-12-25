from flask import Blueprint
from flask_restful import Api

sku_bp = Blueprint('sku', __name__)
sku_api = Api(sku_bp)

from . import views 