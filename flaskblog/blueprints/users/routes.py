from flask import render_template, flash, redirect, url_for, request
from flaskblog import bcrypt, db
from flaskblog.models import User
from flaskblog.blueprints.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestPasswordResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.blueprints.users.utils import is_relative_url, save_profile_picture, delete_old_profile_picture, send_reset_password_email
from flaskblog.blueprints.users import users

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode()
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash(f'your account has been created successfully!', "success")
        return redirect(url_for('posts.home'))

    return render_template("register.html", title="Register", form=form)

@users.route("/login",  methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if login_user(user, form.remember.data):
                next = request.args.get("next")
                if next and is_relative_url(next):
                    return redirect(next)
                else:
                    flash(f'Logged in successfully!', "success")
                    return redirect(url_for('posts.home'))
            else:
                raise Exception("This is not handled as we don't have active or not active in our website.")
        else:
            flash(f'invalid credentials!', "danger")
            # Then it continues to the outer return statement.

    return render_template("login.html", title="Login", form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("posts.home"))

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    
    if form.validate_on_submit():
        
        if form.update_profile_picture.data:
            picture_fn = save_profile_picture(form.update_profile_picture.data)
            delete_old_profile_picture()
            
            current_user.image_file = picture_fn

        current_user.username = form.username.data
        current_user.email = form.email.data
        
        # User.query.filter_by(id=current_user.id).update({User.username: form.username.data, 
        #                                                 User.email: form.email.data})
        
        db.session.commit()
        flash("Your profile has been updated successfully!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template("account.html", title="Account", form=form)

@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('posts.home'))
    
    form = RequestPasswordResetForm()
    
    if form.validate_on_submit():
        send_reset_password_email(form.email.data)
        flash("An email has been sent with instructions to reset the password", "info")
        return redirect(url_for('users.login'))

    return render_template("reset_request.html", title="Reset Password", form=form)

@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('posts.home'))
    
    user = User.verify_reset_password_token(token)
    if not user:
        flash("This is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))

    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        user.password = bcrypt.generate_password_hash(form.password.data)
        db.session.commit()
        
        login_user(user)
        flash("Password has been changed successfully!", 'success')
        return redirect(url_for('posts.home'))

    return render_template("reset_password.html", title="Reset Password", form=form)
