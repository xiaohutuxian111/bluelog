"""
@FileName：auth.py
@Author：stone
@Time：2023/5/10 16:38
@Description:
"""

from flask import Blueprint, render_template, redirect, url_for, flash

from bluelog.models import Admin
from bluelog.forms import LoginForm
from flask_login import login_required, logout_user, login_user,current_user

from bluelog.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=["GET", 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remenber.data
        admin = Admin.query.first()
        if admin:
            # 验证用户和密码
            if username == admin.username and admin.validate_password(password):
                #  登录用户
                login_user(admin, remember)
                flash("欢迎回家", 'info')
                # 返回上一个页面
                return redirect_back()
            flash("密码错误", 'warning')
        else:
            flash("无当前用户名", 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("退出登录", 'info')
    return redirect_back()
