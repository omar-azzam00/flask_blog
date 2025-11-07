from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2), Length(max=20)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired()])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    sign_up = SubmitField("Sign Up")
    
    def validate_username(self, username):
        if User.query.filter_by(username= username.data).first():
            raise ValidationError("Username already exists!")
    
    def validate_email(self, email):
        if User.query.filter_by(email= email.data).first():
            raise ValidationError("Email already exists!")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    login = SubmitField("Log In")
    

images = ["png", "jpg", "jpeg", "webp"]
class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2), Length(max=20)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    update_profile_picture = FileField("Update Profile Picture", validators=[FileAllowed(images, "This is not an image!")])
    update = SubmitField("Update")
    
    def validate_username(self, username):
        if username.data != current_user.username and User.query.filter_by(username= username.data).first():  
            raise ValidationError("Username already exists!")
    
    def validate_email(self, email):
        if email.data != current_user.email and User.query.filter_by(email= email.data).first():
            raise ValidationError("Email already exists!")

class RequestPasswordResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField("Reset Password")
    
    def validate_email(self, email):
        if not User.query.filter_by(email= email.data).first():
            raise ValidationError("This email doesn't exits!")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("New Password", validators=[DataRequired()])
    password_confirm = PasswordField("Confirm New Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Reset Password")