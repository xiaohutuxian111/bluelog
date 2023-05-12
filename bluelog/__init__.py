# """
# @FileName：__init__.py.py
# @Author：stone
# @Time：2023/5/10 16:30
# @Description:初始化函数
# """
# import os
#
# import click
# from flask import Flask, render_template
#
# from bluelog.blueprints.blog import blog_bp
# from bluelog.blueprints.admin import admin_bp
# from bluelog.blueprints.auth import auth_bp
#
# from bluelog.settings import config
# from bluelog.extensions import bootstrap, db, moment, ckeditor, mail
#
#
# def create_app(config_name=None):
#     if config_name is None:
#         config_name = os.getenv('FLASK_CONFIG', 'development')
#
#     app = Flask('bluglog')
#     app.config.from_object(config[config_name])
#     # 注册日志
#     register_logging(app)
#     # 注册扩展
#     register_extensions(app)
#     # 注册蓝本
#     register_blueprints(app)
#     # 注册自定义的shell命令
#     register_commands(app)
#     # 注册错误处理函数
#     register_errors(app)
#     #  注册shell 上下文处理函数
#     register_shell_context(app)
#     #  注册模块上下文处理函数
#     register_template_context(app)
#
#     return app
#
#
# def register_template_context(app):
#     @app.context_processor
#     def make_template_context():
#         pass
#         # admin = Admin.query.first()
#         # categories = Category.query.order_by(Category.name).all()
#         # links = Link.query.order_by(Link.name).all()
#         # return dict(admin=admin, categories=categories, links=links)
#
#
# def register_blueprints(app):
#     app.register_blueprint(blog_bp)
#     app.register_blueprint(admin_bp, url_prefix='/admin')
#     app.register_blueprint(auth_bp, url_prefix='/auth')
#
#
# def register_logging(app):
#     """日志模块"""
#     pass
#
#
# def register_shell_context(app):
#     @app.shell_context_processor
#     def make_shell_context():
#         return dict(db=db)
#
#
# def register_extensions(app):
#     bootstrap.init_app(app)
#     db.init_app(app)
#     ckeditor.init_app(app)
#     mail.init_app(app)
#     moment.init_app(app)
#
#
# def register_errors(app):
#     @app.errorhandler(400)
#     def bad_request(e):
#         return render_template('errors/400.html'), 400
#
#     @app.errorhandler(404)
#     def page_not_found(e):
#         return render_template("errors/404.html"), 404
#
#     @app.errorhandler(500)
#     def internal_server_error(e):
#         return render_template('errors/500.html'), 500
#
#
# def register_commands(app):
#     @app.cli.command()
#     @click.option('--drop', is_flag=True, help="对于创建的数据库进行清空")
#     def initdb(drop):
#         """初始化数据库"""
#         if drop:
#             click.confirm("数据库将要被删除,确定你要这样操作：", abort=True)
#             db.drop_all()
#             click.echo("已经删除数据库")
#         db.create_all()
#         click.echo("数据库已经创建成功")
#
#     @app.cli.command()
#     @click.option('--category', default=10, help='创建分类信息默认为10条')
#     @click.option('--post', default=50, help='创建内容,默认为50条')
#     @click.option('--comment', default=200, help='创建评论信息,默认为500条')
#     def forge(category, post, comment):
#         """生成数据库信息"""
#         from bluelog.fakes import fake_admin, fake_categories, fake_posts, fake_comments, fake_links
#
#         db.drop_all()
#         db.create_all()
#
#         click.echo("创建admin用户")
#         fake_admin()
#
#         click.echo("创建{}条文章分类".format(category))
#         fake_categories(category)
#
#         click.echo('创建{}条文章'.format(post))
#         fake_posts()
#
#         click.echo('创建{}评论'.format(comment))
#         fake_comments()
#
#         click.echo("创建文章链接")
#         fake_links()
#
#         click.echo("数据生成完成")



import os

import click
from flask import Flask, render_template

from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.blog import blog_bp
from bluelog.extensions import bootstrap, db, ckeditor, mail, moment
from bluelog.models import Admin, Post, Category, Comment, Link
from bluelog.settings import config

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('bluelog')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)
    return app


def register_logging(app):
    pass


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')

1
def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Post=Post, Category=Category, Comment=Comment)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        links = Link.query.order_by(Link.name).all()
        return dict(admin=admin, categories=categories, links=links)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        """Generate fake data."""
        from bluelog.fakes import fake_admin, fake_categories, fake_posts, fake_comments, fake_links

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)

        click.echo('Generating links...')
        fake_links()

        click.echo('Done.')
