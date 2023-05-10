"""
@FileName：__init__.py.py
@Author：stone
@Time：2023/5/10 16:30
@Description:初始化函数
"""
import os
from flask import Flask

from bluelog.blueprints import blog, admin, auth
from bluelog.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('bluglog')
    app.config.from_object(config(config_name))

    app.register_blueprint(blog)
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(auth, url_prefix='/auth')
    return app
