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
    role = db.relationship('Role', backref='user', passive_deletes=True)
    exercise = db.relationship('Exercise', backref='user', passive_deletes=True)
    submission = db.relationship('Submission', backref='user', passive_deletes=True)

class Role(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    role = db.Column(db.String(150))
    
class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(150), unique=False)
    description_file_name = db.Column(db.String(150))
    description_file_data = db.Column(db.LargeBinary)
    countdown = db.Column(db.String(150))
    solution = db.Column(db.String(150))
    testcase = db.relationship('TestCase', backref='exercise', passive_deletes=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    submission = db.relationship('Submission', backref='exercise', passive_deletes=True)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(250))
    score = db.Column(db.String(150))
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input = db.Column(db.String(150), unique=True)
    output = db.Column(db.String(150), unique=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())