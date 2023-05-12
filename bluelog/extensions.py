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

bootstrap = Bootstrap()
db = SQLAlchemy()
ckeditor = CKEditor()
moment = Moment()
mail = Mail()
