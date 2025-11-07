from flask import Blueprint

posts = Blueprint('posts', __name__)

import flaskblog.blueprints.posts.routes