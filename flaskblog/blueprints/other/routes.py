from flask import  render_template
from flaskblog.blueprints.other import other

@other.route("/about")
def about():
    return render_template("about.html", title="About")
