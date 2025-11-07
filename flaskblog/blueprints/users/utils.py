from flask import url_for, render_template, current_app
from flaskblog import login_manager
import secrets, os
from PIL import Image
from urllib.parse import urlparse
from flaskblog.models import User
from flask_mailman import EmailMessage
from flask_login import current_user

@login_manager.user_loader
def load_user(user_id):
    # raise Exception("Let's break the fucking server")
    return User.query.get(int(user_id))

def is_relative_url(url):
    paresed = urlparse(url)
    return not paresed.scheme and not paresed.netloc


def is_relative_url(url):
    paresed = urlparse(url)
    return not paresed.scheme and not paresed.netloc

def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(20) 
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    picture_path = os.path.join(current_app.static_folder, 'profile_pics', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def delete_old_profile_picture():
    if current_user.image_file != User.image_file.default.arg:
        try:
            old_picture_path = os.path.join(current_app.static_folder, 'profile_pics', current_user.image_file)
            os.remove(old_picture_path)
        except FileNotFoundError:
            # if the file was already for some reason removed then we should simply continue.
            pass


def send_reset_password_email(email):
    token = User.get_reset_password_token(email)
    url = url_for("users.reset_password", token=token, _external=True)
    content = render_template("reset_password_email.html", url=url)
    msg = EmailMessage("Flaskblog Reset Password", content, to=[email])
    msg.content_subtype = "html"
    msg.send()

# def apply_login_required_fingerprint():
#     # you can check if a specific view function has the login_required decorator applied to it using
#     # view_func.getattr("login_required_fingerprint") => True | None

#     # Note That You have to add the @login_required decorator after the @app.route(...) decorator
#     # in order for this function to work properly
#     original_login_required = flask_login.login_required

#     def fingerprint_login_required(func):
#         new_func = original_login_required(func)
#         new_func.login_required_fingerprint = True
#         return new_func
    
#     flask_login.login_required = fingerprint_login_required