from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
from exts import mail, db
from flask_mail import Message
from models import EmailCpatcharModel, UserModel, QuestionModel, AnswerModel
import string
import random
from datetime import datetime
from blueprints.forms import RegisterForm, LoginForm, QuestionForm, AnswerForm, ChangeForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from logintest import login_manager
from flask_login import login_required, login_user, logout_user, current_user
from .check import *

bp = Blueprint("user1", __name__, url_prefix="/")

login_manager.session_protection = 'basic'
login_manager.login_view = 'user1.login'
login_manager.login_message = u"请先登录。"


@bp.route("/")
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template("index.html", questions=questions)


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                login_user(user)  # 关键就是 login_user(curr_user) 这句代码，之前要构建 User 对象，并指定 id。
                # session['user_id'] = user.id
                # session['username'] = user.username
                return redirect("/")
            else:
                flash("邮箱和密码不匹配!")
                return redirect(url_for("user1.login"))
        else:
            flash("邮箱或者密码格式不对!")
            return redirect(url_for("user1.login"))


@bp.route('/logout')
def logout():
    # 退出
    logout_user()
    return redirect(url_for("user1.login"))


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            hash_password = generate_password_hash(password)

            user = UserModel(username=username, email=email, password=hash_password)

            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user1.login"))
        else:
            print(form.errors)
            flash(form.errors)

            return redirect(url_for("user1.register"))


@bp.route("/captcha", methods=['POST'])
def get_captcha():
    # 默认get方法args   POST
    email = request.form.get("email")
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters, 4))
    email1 = UserModel.query.filter_by(email=email).first()
    if check_email_url(email=email):
        return jsonify({"code": 5002, "message": "请输入正确的邮箱"})
    if email1:
        return jsonify({"code": 5001, "message": "邮箱已经注册，请切换邮箱注册"})
    elif email:
        message = Message(
            subject="邮箱测试",
            recipients=[email],
            body=f"您的注册码是：{captcha}.不要告诉任何人"
        )
        # print(captcha)
        mail.send(message)
        captcha_model = EmailCpatcharModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCpatcharModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()

        return jsonify({"code": 200, "message": "验证码发生成功"})
    else:
        return jsonify({"code": 400, "message": "请先输入邮箱"})


@bp.route("/public", methods=['GET', 'POST'])
@login_required
def public_question():
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=current_user)
            db.session.add(question)
            db.session.commit()
            return redirect('/')
        else:
            flash("标题或内容格式错误！")
            return redirect(url_for("user1.public_question"))


@bp.route("/question/<int:question_id>")
def question_detail(question_id):
    question = QuestionModel.query.get(question_id)
    return render_template("detail.html", question=question)


@bp.route("/answer/<int:question_id>", methods=['POST'])
@login_required
def answer(question_id):
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        answer_model = AnswerModel(content=content, author=current_user, question_id=question_id)
        db.session.add(answer_model)
        db.session.commit()
        return redirect(url_for("user1.question_detail", question_id=question_id))
    else:
        flash("表单验证失败")
        return redirect(url_for("user1.question_detail", question_id=question_id))


@bp.route('/search')
def search():
    q = request.args.get("q")
    questions = QuestionModel.query.filter(or_(QuestionModel.title.contains(q), QuestionModel.content.contains(q))) \
        .order_by(QuestionModel.create_time.desc())
    return render_template("index.html", questions=questions)


@bp.route('/core', methods=['GET', 'POST'])
@login_required
def core():
    return render_template("core.html")


@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'GET':
        return render_template("change_password.html")
    else:
        form = ChangeForm(request.form)
        if form.validate():
            password1 = UserModel.query.filter_by(email=current_user.email).first()
            change_password1 = form.change_password.data
            change_password2 = form.change_password1.data
            hash_password = generate_password_hash(change_password1)

            if check_password_hash(password1.password, change_password1):
                flash("不能跟原始密码一样")
                return redirect(url_for("user1.change_password"))
            else:
                print(change_password1, change_password2)
                user = UserModel.query.filter(UserModel.email == current_user.email).\
                    update({UserModel.password: hash_password})

                # suer = UserModel.query.filter_by(email=current_user.email).first()
                # suer.password = hash_password
                db.session.commit()

                return redirect(url_for("user1.index"))
        else:
            print(form.change_password1.errors)
            flash(form.errors)
            return redirect(url_for("user1.change_password"))
