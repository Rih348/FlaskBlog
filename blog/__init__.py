from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///web.db"

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from blog.user.routes import end_user
    from blog.post.routes import posts_
    from blog.main.routes import main
    app.register_blueprint(end_user)
    app.register_blueprint(posts_)
    app.register_blueprint(main)

    return app