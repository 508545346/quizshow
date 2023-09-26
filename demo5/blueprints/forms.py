# -*- coding:UTF-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, IntegerField, ValidationError, Form
from wtforms.validators import DataRequired, EqualTo, Length, email, InputRequired
from models import EmailCpatcharModel, UserModel


class LoginForm(Form):
    email = StringField(validators=[email()])
    password = StringField(validators=[Length(min=6, max=20)])


class RegisterForm(Form):
    username = StringField(validators=[Length(min=3, max=20)])
    email = StringField(validators=[email()])
    captcha = StringField(validators=[Length(min=4, max=4)])
    password = StringField(validators=[Length(min=6, max=20)])
    password_confirm = StringField(validators=[DataRequired(), EqualTo("password", message="两次密码必须一致")])

    # submit = SubmitField('立即注册')

    def validate_captcha(self, field):
        # 获取界面上面的邮箱然后去匹配数据库里面的验证码是否正确
        captcha = field.data
        email1 = self.email.data
        captcha_model = EmailCpatcharModel.query.filter_by(email=email1).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            raise ValidationError("邮箱验证码错误！")

    def validate_email(self, field):
        email1 = field.data
        if email1:
            user_model = UserModel.query.filter_by(email=email1).first()
            if user_model:
                raise ValidationError("邮箱已经存在")
        else:
            raise ValidationError("输入邮箱")

    def validate_username(self, field):
        username = field.data
        print(username)
        if len(username) < 3 or len(username) > 20:
            raise ValidationError("用户名长度超出限制")


class QuestionForm(Form):
    title = StringField(validators=[Length(min=3, max=200)])
    content = StringField(validators=[Length(min=5)])


class AnswerForm(Form):
    content = StringField(validators=[Length(min=1)])


class ChangeForm(Form):
    change_password = StringField(validators=[Length(min=6, max=20)])
    # change_password1 = StringField(validators=[Length(min=6, max=20)])
    change_password1 = StringField(validators=[DataRequired(), EqualTo("change_password", message="两次密码必须一致")])

