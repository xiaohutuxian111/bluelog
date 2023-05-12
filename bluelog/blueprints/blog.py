"""
@FileName：blog.py
@Author：stone
@Time：2023/5/10 16:38
@Description:
"""

from flask import Blueprint, render_template, request, current_app
from  bluelog.models import  Post

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('blog/index.html',posts=posts)


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    return render_template('blog/category.html')


@blog_bp.route('/post/<int:post_id>', methods=["GET", "POST"])
def show_post(post_id):
    return render_template("blog/post.html")
