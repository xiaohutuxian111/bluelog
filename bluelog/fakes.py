"""
@FileName：fakes.py
@Author：stone
@Time：2023/5/10 16:36
@Description:沈城数据库数据
"""
import random

from faker import Faker
from bluelog.extensions import db

from bluelog.models import Admin, Category, Post, Comment, Link

fake = Faker(locale='zh_CN')


def fake_admin():
    """生成admin数据"""
    admin = Admin(
        username='admin',
        blog_title="Bluelog",
        blog_sub_title='No，I am real thing',
        name='Hima',
        about='哈哈没有内容'
    )
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):
    """生成文章分类数据"""
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except InterruptedError:
            db.session.rollback()


def fake_posts(count=50):
    """生成文章数据"""
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()


def fake_comments(count=500):
    """生成评论数据"""
    for _ in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    salt = int(count * 0.1)
    for _ in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
        # from admin
        comment = Comment(
            author='Mima Kirigoe',
            email='mima@example.com',
            site='example.com',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()


def fake_links():
    twitter = Link(name='Twitter', url='#')
    facebook = Link(name='Facebook', url='#')
    linkedin = Link(name='LinkedIn', url='#')
    google = Link(name='Google+', url='#')
    db.session.add_all([twitter, facebook, linkedin, google])
    db.session.commit()
