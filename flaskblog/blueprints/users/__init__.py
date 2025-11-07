from flask import Blueprint

users = Blueprint('users', __name__)

import flaskblog.blueprints.users.routes