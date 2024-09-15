from flask import Blueprint
from flask_restx import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp, version='1.0', title='Benefits API', description='API for calculating employee benefits')

from .employee_routes import ns as employee_ns

api.add_namespace(employee_ns)
