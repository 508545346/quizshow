# 数据库的配置信息
db_url = "mysql+pymysql://root:123456789@127.0.0.1/student"
SQLALCHEMY_DATABASE_URI = db_url
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "123"


# 邮箱设置

MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = "508545346@qq.com"
MAIL_PASSWORD = "dbnmpxiruwbzcagg"
MAIL_DEFAULT_SENDER = "508545346@qq.com"


