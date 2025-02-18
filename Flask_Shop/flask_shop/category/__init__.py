from flask import Blueprint
from flask_restful import Api
category_bp = Blueprint('category', __name__)
category_api = Api(category_bp)

attribute_bp = Blueprint('attribute', __name__)
attribute_api = Api(attribute_bp)


from. import views



