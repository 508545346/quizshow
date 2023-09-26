from flask import Blueprint, render_template
# from demo5.decorators import login_required

bp = Blueprint("qa", __name__, url_prefix="/")


# @bp.route("/public")
# @login_required
# def public_question():
#     return render_template("public_question.html")



#
# # @bp.route('/')
# # def index():
# #     return render_template('login1.html')
#
#
# @bp.route('/', methods=['POST', 'GET'])
# def login():
#     form = Login()
#     print(form.username, form.password)
#     print(form.validate_on_submit())
#     error_msg = ''
#     account1 = account.query.filter().all()
#     # for i in account1:
#     #     print(i.username, i.password)
#     if request.method == "GET":
#         username = request.args.get('username')
#         password = request.args.get('password')
#     else:
#         username = request.form.get('username')
#         password = request.form.get('password')
#
#     print('username:%s,password:%s' % (username, password))
#     for i in account1:
#         if username and password:
#             if username == i.username and int(password) == i.password:
#                 return redirect('/list')
#             else:
#                 flash("账号和密码不对")
#                 # error_msg = '账号和密码不对'
#         else:
#             flash("需要用户名和密码")
#             # error_msg = '需要用户名和密码'
#
#     return render_template('login2.html')
#
#
# @bp.route('/list/')
# def userlist():
#     userlist1 = account.query.filter().all()
#     return render_template('list.html', userlist=userlist1)
#
#
# @bp.route('/update/')
# def update():
#     username = request.args.get('username')  # 前端传递过来的需要修改的username
#
#     return render_template('update.html', user=username)  # user传到到update.html页面
#
#
# @bp.route('/updateaction/', methods=['POST'])
# def updateaction():
#     params = request.args if request.method == 'GET' else request.form
#
#     username = params.get('username')
#     password = params.get('password')
#     xiugai = account.query.filter(account.username == username).first()
#     if xiugai.password == int(password):
#         return render_template('update.html', user=username, error_msg='密码一样，重新输入')
#     else:
#         xiugai1 = account.query.filter(account.username == username).first()
#         xiugai1.password = int(password)
#         db.session.commit()
#         return redirect('/list')
#
#
# @bp.route('/add/')
# def add():
#     return render_template('add.html')
#
#
# @bp.route('/addaction/', methods=['POST'])
# def addaction():
#     params = request.args if request.method == 'GET' else request.form
#     username = params.get('username')
#     password = params.get('password')
#     # 通过username进行查找，如果为空的话就可以新增，不为空就是存在该账号
#     user = account.query.filter(account.username == username).all()
#
#     if username == '':
#         return render_template('add.html', error_msg='请输入账号')
#     elif password == '':
#         return render_template('add.html', error_msg='请输密码')
#
#     if user:
#         return render_template('add.html', error_msg='账号已存在')
#     else:
#         add1 = account(username=username, password=int(password))
#         db.session.add(add1)
#         db.session.commit()
#         return redirect('/list')
#
#
# @bp.route('/delete', methods=['POST', 'GET'])
# def delete():
#     username = request.args.get('username')
#     # 通过前端传递过来的数据进行删除
#     account.query.filter(account.username == username).delete()
#     db.session.commit()
#     return redirect('/list')
#
