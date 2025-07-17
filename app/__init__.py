from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_mail import Mail


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
moment = Moment()
mail = Mail()

bts = Bootstrap5()
ckeditor = CKEditor()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app)
    login.init_app(app)
    moment.init_app(app)
    mail.init_app(app)

    bts.init_app(app)
    ckeditor.init_app(app)



    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.email import bp as email_bp
    app.register_blueprint(email_bp)

    from app.blog import bp as blog_bp
    app.register_blueprint(blog_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app


from app import models