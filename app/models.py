from datetime import datetime
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(70), nullable=False)
    name = db.Column(db.String(70), nullable=False)
    slug = db.Column(db.String(70), nullable=False)
    about_me = db.Column(db.String(300), nullable=True, default=" ")
    password_hash = db.Column(db.String(300), nullable=False)
    img_url = db.Column(db.String(100), nullable=False, default="avatar.png")
    posts = db.relationship('Posts',cascade="all, delete", order_by="Posts.date.desc()", backref='author', lazy=True)
    comments = db.relationship('Comments',cascade="all, delete", backref='author', lazy=True)

postscategories = db.Table('postscategories',
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), nullable=False),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), nullable=False))

class Posts(db.Model):
    __searchable__ = ['title', 'content']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(50), nullable=False)
    views = db.Column(db.Integer, nullable=False, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(3000), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    categories = db.relationship('Categories', cascade="all, delete", secondary=postscategories, lazy='subquery', backref=db.backref('posts', cascade="all, delete", order_by="Posts.date.desc()", lazy=True))
    comments = db.relationship('Comments', cascade="all, delete", order_by="Comments.date.desc()", backref="post", lazy=True)

class Categories(db.Model) :
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    slug = db.Column(db.String(70), nullable=False)

class Comments(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    replies = db.relationship('Comments', cascade="all, delete", order_by="Comments.date.desc()", backref=db.backref("parent", remote_side=[id]), lazy=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("comments.id"))

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())
