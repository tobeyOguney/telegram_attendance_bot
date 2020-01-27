from flask_restplus import Api
from flask import Blueprint

from .main.controllers.attendance_controller import api as attendance_ns
from .main.controllers.user_controller import api as user_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='TELEGRAM ATTENDANCE SYSTEM API',
          version='1.0',
          description='a web service for telegram group attendance'
          )

api.add_namespace(attendance_ns, path='/attendance')
api.add_namespace(user_ns, path='/user')