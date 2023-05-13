"""
@FileName：admin.py
@Author：stone
@Time：2023/5/10 16:38
@Description:
"""

from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from bluelog.forms import SettingsForm, PostForm, CategoryForm, LinkForm
from bluelog.utils import redirect_back
from bluelog.models import Post, Category, Comment
from flask_login import current_user, login_required
from bluelog.extensions import db

admin_bp = Blueprint('admin', __name__)


#
# @admin_bp.before_request
# @login_required
# def login_protect():
#     """保证使用admin蓝图都要已登录"""
#     pass


@admin_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingsForm()
    return render_template('admin/settings.html', form=form)


@admin_bp.route('/post/manage')
@login_required
def manage_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=current_app.config[
        'BLUELOG_MANAGE_POST_PER_PAGE'])
    posts = pagination.items

    return render_template('admin/manage_post.html', pagination=pagination, posts=posts)


@admin_bp.route('/post/new', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, body=body, category=category)
        db.session.add(post)
        db.session.commit()
        flash("文章添加成功", 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)


@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash("修改文章成功"'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('admin/edit_post.html', form=form)


@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("文章已经删除", 'success')
    return redirect_back()


@admin_bp.route('/post/<int:post_id>/set-comment', methods=['POST'])
@login_required
def set_comment(post_id):
    post =  Post.query.get_or_404(post_id)
    if post.can_comment:
        post.can_comment=False
        flash("关闭评论功能",'success')
    else:
        post.can_comment = True
        flash("开启评论功能", 'success')
    db.session.commit()
    return redirect_back()


@admin_bp.route('/comment/manage')
@login_required
def manage_comment():
    # 从查询字符串中获取过滤规则
    filter_rule =  request.args.get('filter','all')
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    if  filter_rule == 'unread':
        filter_comments = Comment.query.filter_by(reviewed=False)
    elif  filter_rule == 'admin':
        filter_comments = Comment.query.filter_by(from_admin=True)
    else:
        filter_comments = Comment.query
    pagination = filter_comments.order_by(Comment.timestamp.desc()).paginate(page=page,per_page=per_page)
    comments = pagination.items

    return render_template('admin/manage_comment.html',comments=comments,pagination=pagination)


@admin_bp.route('/comment/<int:comment_id>/approve', methods=['POST'])
@login_required
def approve_comment(comment_id):
    comment= Comment.query.get_or_404(comment_id)
    comment.reviewed =True
    db.session.commit()
    flash("评论可以发布",'success')
    return redirect_back()


@admin_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash("评论已经删除",'success')
    return redirect_back()


@admin_bp.route('/category/manage')
def manage_category():
    return render_template('admin/manage_category.html')


@admin_bp.route('/category/new', methods=['GET', 'POST'])
def new_category():
    form = CategoryForm()
    return render_template('admin/new_category.html', form=form)


@admin_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def edit_category(category_id):
    form = CategoryForm()
    return render_template('admin/edit_category.html', form=form)


@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    return redirect(url_for('.manage_category'))


@admin_bp.route('/link/manage')
def manage_link():
    return render_template('admin/manage_link.html')


@admin_bp.route('/link/new', methods=['GET', 'POST'])
def new_link():
    form = LinkForm()
    return render_template('admin/new_link.html', form=form)


@admin_bp.route('/link/<int:link_id>/edit', methods=['GET', 'POST'])
def edit_link(link_id):
    form = LinkForm()
    return render_template('admin/edit_link.html', form=form)


@admin_bp.route('/link/<int:link_id>/delete', methods=['POST'])
def delete_link(link_id):
    return redirect(url_for('.manage_link'))
