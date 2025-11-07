from flaskblog import db, RESET_PASSWORD_MAX_AGE
from flask_login import UserMixin
from flaskblog import reset_password_serializer_wrapper


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = "default.jpg")
    password = db.Column(db.String(60), nullable = False)
    posts = db.relationship('Post', backref="author", lazy=True)
    
    @staticmethod
    def get_reset_password_token(email):
        user = User.query.filter_by(email=email).first()
        return reset_password_serializer_wrapper['value'].dumps({
            "id": user.id,
        })

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = reset_password_serializer_wrapper['value'].loads(token, max_age=RESET_PASSWORD_MAX_AGE)['id']
            return User.query.get_or_404(id)
        except:
            return None

    # this is  a magic method that tells what to show when the object is printed out.
    def __repr__(self):
        return f"User#{self.id}('{self.username}', '{self.email}', '{self.image_file}', '{self.password}')"

from flaskblog import db
from datetime import datetime, timezone

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default=lambda:datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    
    def __repr__(self):
        return f"post#{self.id}('{self.title}', '{self.date_posted}')"