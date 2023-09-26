import config
from flask import Flask
from exts import db, mail
from blueprints import qa_bp
from blueprints import user_bp
from flask_migrate import Migrate
from logintest import login_manager


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
login_manager.init_app(app)
migrate = Migrate(app, db)


app.register_blueprint(user_bp)
# app.register_blueprint(qa_bp)


if __name__ == '__main__':
    app.run(debug=True)

