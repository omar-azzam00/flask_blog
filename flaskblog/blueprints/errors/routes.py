from flaskblog.blueprints.errors import errors
from flask import render_template
import werkzeug.exceptions

# 400 error code
@errors.app_errorhandler(werkzeug.exceptions.HTTPException)
def http_handler(e):
    return render_template("error.html", error_title=e.code, error_desc=e.description, no_sidebar=True), e.code

# @errors.app_errorhandler(werkzeug.exceptions.Forbidden)
# def forbidden_handler(e):
#     error_title="Permission Denied" 
#     error_desc="You can't perform this action"
#     return render_template("error.html", error_title=error_title, error_desc=error_desc, no_sidebar=True), e.code

# @errors.app_errorhandler(werkzeug.exceptions.NotFound)
# def not_found_handler(e):
#     error_title = "Page Not Found"
#     error_desc = "The page you are looking for does not exist."
#     return render_template("error.html", error_title=error_title, error_desc=error_desc, no_sidebar=True), e.code

# @errors.app_errorhandler(werkzeug.exceptions.InternalServerError)
# def internal_server_error_handler(e):
#     error_title = "Internal Server Error"
#     error_desc = "An unexpected error occurred. Please try again later."
#     return render_template("error.html", error_title=error_title, error_desc=error_desc, no_sidebar=True), e.code
