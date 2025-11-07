from flask import Blueprint

other = Blueprint("other", __name__)

import flaskblog.blueprints.other.routes