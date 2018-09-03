from flask import Flask
from config import config

# bootstrap = Bootstrap()
# mail = Mail()
# moment = Moment()
# db = SQLAlchemy()
# pagedown = PageDown()
#
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # bootstrap.init_app(app)
    # mail.init_app(app)
    # moment.init_app(app)
    # login_manager.init_app(app)
    # pagedown.init_app(app)

    # if app.config['SSL_REDIRECT']:
    #     from flask_sslify import SSLify
    #     sslify = SSLify(app)

    from app.main import main as main_routes
    from app.api import api as api_routes



    app.register_blueprint(main_routes)
    app.register_blueprint(api_routes, url_prefix='/api')


    # from .auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')
    #学习使人进步
    # from .api import api as api_blueprint
    # app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app


if __name__ == '__main__':
    app = create_app('development')
    app.run()