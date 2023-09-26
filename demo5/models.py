# -*- coding:UTF-8 -*-
from exts import db
from datetime import datetime
from logintest import login_manager
from flask_login import UserMixin


class EmailCpatcharModel(db.Model):
    """数据库映射的表"""
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class UserModel(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def get_id(self):
        return self.id


class QuestionModel(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("UserModel", backref="questions")


class AnswerModel(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    question = db.relationship("QuestionModel", backref=db.backref("answers", order_by=create_time.desc()))
    author = db.relationship("UserModel", backref="answers")


# user session 记录的是用户 ID (user_id)，回调函数的作用就是通过 user_id 返回对应的 User 对象。user_loader 回调函数在 user_id
# 非法的时候不应该抛出异常，而要返回 None。没有这个回调函数的话，Flask-Login 将无法工作
@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(id)


