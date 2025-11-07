from flask import Blueprint

errors = Blueprint('errors', __name__)

import flaskblog.blueprints.errors.routes