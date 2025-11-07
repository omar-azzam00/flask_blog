from flask import render_template, flash, redirect, url_for, request, abort
from flaskblog import db, DEFAULT_POSTS_PER_PAGE, MAX_POSTS_PER_PAGE
from flaskblog.models import User, Post
from flaskblog.blueprints.posts.forms import PostForm
from flask_login import current_user, login_required
from flaskblog.blueprints.posts import posts


@posts.route("/")
@posts.route("/home")
@posts.route("/posts")
# This is a called a view function
def home():
    # page_number = request.args.get("page", 1, type=int)
    # posts = Post.query.paginate(per_page=POSTS_PER_PAGE, page=page_number)
    
    try:
        per_page = int(request.args.get("per_page", DEFAULT_POSTS_PER_PAGE))
        
        # we want to display the abort with 400 if page is not an int.
        # as the default behavior returns 404 which is not that accurate
        int(request.args.get('page', 0))
    except:
        abort(400, "your request is bad...maybe invalid query parameters")
    
    posts_page = Post.query.order_by(Post.date_posted.desc())

    username = request.args.get("username")
    if username:
        user_id = User.query.filter_by(username=username).first_or_404(f"this user '{username}' doesn't exist!").id
        posts_page = posts_page.filter_by(user_id=user_id)

    posts_page = posts_page.paginate(per_page=per_page, max_per_page=MAX_POSTS_PER_PAGE)

    return render_template("home.html", posts_page=posts_page)
@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def post_new():
    form = PostForm()
    
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        
        db.session.add(post)
        db.session.commit()
        
        flash("Your post has been created successfully!", "success")
        return redirect(url_for("posts.home"))

    return render_template("post_touch.html", title="New Post", form=form, legend="Create Post", button="Post")

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id, "This post doesn't exist!")
    return render_template("post.html", title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id, "This post doesn't exist!")
    
    if post.author.id != current_user.id:
        # Permission Denied Response
        abort(403, description="This is not your post!")
    
    form = PostForm()
    
    if form.validate_on_submit():
        # this is another way to perform the update thing
        Post.query.filter_by(id=post.id).update({"title": form.title.data, "content": form.content.data})
        Post.query.session.commit()
        
        flash("Post updated successfully!", "success")
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template("post_touch.html", title=post.title, form=form, legend="Update Post", button="Update")

@posts.route("/post/<int:post_id>/delete", methods=["GET", "POST"])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id, "This post doesn't exist!")
    
    if post.author.id != current_user.id:
        # Permission Denied Response
        abort(403, description="This is not your post!")
    
    if request.method == "GET":
        return redirect(url_for("posts.post", post_id=post.id))

    Post.query.filter_by(id=post.id).delete()
    Post.query.session.commit()

    flash("The post has been deleted!", "danger")
    return redirect(url_for("posts.home"))

# @posts.route("/posts/<username>")
# # This is a called a view function
# def user_posts(username):
#     try:
#         per_page = int(request.args.get("per_page", DEFAULT_POSTS_PER_PAGE))
#     except:
#         abort(404)

#     user =  User.query.filter_by(username=username).first_or_404()

#     posts_page = Post.query.filter_by(user_id=user.id).\
#                             order_by(Post.date_posted.desc()).\
#                             paginate(per_page=per_page, max_per_page=MAX_POSTS_PER_PAGE)

#     return render_template("home.html", posts_page=posts_page, per_page_query=request.args.get("per_page"), title=f"{username} posts")