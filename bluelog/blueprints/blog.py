"""
@FileName：blog.py
@Author：stone
@Time：2023/5/10 16:38
@Description:
"""

from flask import Blueprint, render_template, request, current_app, url_for, flash, redirect, abort, make_response
from bluelog.forms import AdminCommentForm, CommentForm
from bluelog.models import Post, Category, Comment
from bluelog.extensions import db
from bluelog.emails import send_new_comment_email, send_new_reply_email
from bluelog.utils import redirect_back
from flask_login import current_user

blog_bp = Blueprint('blog', __name__)


@blog_bp.route("/", defaults={'page': 1})
@blog_bp.route('/page/<int:page>')
def index(page):
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    # 查询字符串获取当前的页数
    # page  = request.args.get('page',1,type=int)
    #  每页数量
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    #  分页对象
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page)
    # 当前页数的记录列表
    posts = pagination.items
    return render_template('blog/index.html', pagination=pagination, posts=posts)


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category, pagination=pagination, posts=posts)


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.first_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).order_by(Comment.timestamp.asc()).paginate(page=page,
                                                                                            per_page=per_page)
    comments = pagination.items

    #  当前用户已经登录，使用管理员
    # if current_app.is_authenticated:
    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_app.name
        form.email.data = current_app.config['BLUELOG_EMAIL']
        form.site.data = url_for('.index')
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(
            author=author, email=email, site=site, body=body, from_admin=from_admin, post=post, reviewed=reviewed)
        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            send_new_reply_email(replied_comment)
        db.session.add(comment)
        db.session.commit()
        # 根据不同的状态显示不同提示
        if current_user.is_authenticated:
            flash('评论已经添加成功')
        else:
            flash("谢谢,你的评论已经提交管理员审批")
            # 发邮件给管理员
            send_new_comment_email(post)
        return redirect(url_for('.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, form=form, pagination=pagination, comments=comments)


@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.post.can_comment:
        flash("评论未开启", 'warning')
        return redirect(url_for('.show_post', post_id=comment.post_id))
    return redirect(url_for('.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) +
                    '#comment-form')


@blog_bp.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['BLUELOG_THEMES'].keys():
        abort(404)
    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=30 * 24 * 60 * 60)
    return response
