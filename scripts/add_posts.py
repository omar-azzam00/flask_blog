from flaskblog import app
from flaskblog.models import Post

with app.app_context():
    flag = 1
    for i in range(20):
        title = f"Post {str(i + 1)}"
        content = f"This is post {str(i + 1)} content"
        post = Post(title=title, content=content, user_id=flag)
        Post.query.session.add(post)
        Post.query.session.commit()
        flag = 1 if flag == 2 else 2