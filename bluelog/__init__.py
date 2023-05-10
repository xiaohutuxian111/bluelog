"""
@FileName：__init__.py.py
@Author：stone
@Time：2023/5/10 16:30
@Description:初始化函数
"""
import os

import click
from flask import Flask, render_template

from bluelog.blueprints.blog import blog_bp
from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.auth import auth_bp

from bluelog.settings import config
from bluelog.extensions import bootstrap, db, moment, ckeditor, mail


def register_template_context(app):
    pass


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('bluglog')
    app.config.from_object(config[config_name])
    # 注册日志
    register_logging(app)
    #  注册蓝本
    register_blueprints(app)
    # 注册扩展
    register_extensions(app)
    # 注册自定义的shell命令
    register_commands(app)
    # 注册错误处理函数
    register_errors(app)
    #  注册shell 上下文处理函数
    register_shell_context(app)
    #  注册模块上下文处理函数
    register_template_context(app)

    return app


def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_logging(app):
    """日志模块"""
    pass


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help="对于创建的数据库进行清空")
    def initdb(drop):
        """初始化数据库"""
        if drop:
            click.confirm("数据库将要被删除,确定你要这样操作：", abort=True)
            db.drop_all()
            click.echo("已经删除数据库")
        db.create_all()
        click.echo("数据库已经创建成功")

    @app.cli.command()
    @click.option('--category', default=10, help='创建分类信息默认为10条')
    @click.option('--post', default=50, help='创建内容,默认为50条')
    @click.option('--comment', default=200, help='创建评论信息,默认为500条')
    def forge(category, post, comment):
        """生成数据库信息"""
        from bluelog.fakes import fake_admin, fake_categories, fake_posts, fake_comments, fake_links

        db.drop_all()
        db.create_all()

        click.echo("创建admin用户")
        fake_admin()

        click.echo("创建{}条文章分类".format(category))
        fake_categories(category)

        click.echo('创建{}条文章'.format(post))
        fake_posts()

        click.echo('创建{}评论'.format(comment))
        fake_comments()

        click.echo("创建文章链接")
        fake_links()

        click.echo("数据生成完成")
