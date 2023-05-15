from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    professor_token = db.Column(db.String(150), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    exercise = db.relationship('Exercise', backref='user', passive_deletes=True)
    # comments = db.relationship('Comment', backref='user', passive_deletes=True)
    # likes = db.relationship('Like', backref='user', passive_deletes=True)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(150), unique=False)
    solution = db.Column(db.String(150), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.Text, nullable=False)
#     date_created = db.Column(db.DateTime(timezone=True), default=func.now())
#     author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
#     comments = db.relationship('Comment', backref='post', passive_deletes=True)
#     likes = db.relationship('Like', backref='post', passive_deletes=True)

# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.Text, nullable=False)
#     date_created = db.Column(db.DateTime(timezone=True), default=func.now())
#     author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)

# class Like(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     date_created = db.Column(db.DateTime(timezone=True), default=func.now())
#     author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)
