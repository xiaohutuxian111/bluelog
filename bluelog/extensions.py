"""
@FileName：extensions.py
@Author：stone
@Time：2023/5/10 16:37
@Description:扩展实例化
"""
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_login import LoginManager

bootstrap = Bootstrap()
db = SQLAlchemy()
ckeditor = CKEditor()
moment = Moment()
mail = Mail()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from bluelog.models import Admin
    user = Admin.query.get(int(user_id))
    return user



login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'