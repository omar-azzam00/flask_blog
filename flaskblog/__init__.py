from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer
from flask_mailman import Mail
from flaskblog.config import Config

# Extensions 
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = "info"

# Serializers
reset_password_serializer_wrapper = {}

# Constants
DEFAULT_POSTS_PER_PAGE = 5
MAX_POSTS_PER_PAGE = 20
RESET_PASSWORD_MAX_AGE = 86400 # Seconds which means 1 day

def create_app(config_obj=Config()):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    import flaskblog.blueprints as b
    app.register_blueprint(b.other)
    app.register_blueprint(b.posts)
    app.register_blueprint(b.users)
    app.register_blueprint(b.errors)
    
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    
    global reset_password_serializer_wrapper
    reset_password_serializer_wrapper['value'] = URLSafeTimedSerializer(app.config["SECRET_KEY"], salt="reset_password")
    
    return app
