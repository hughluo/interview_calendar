from flask import Flask
from config import config
from utils import log


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    log('hello world')

    from app.main import main as main_routes
    from app.api import api as api_routes

    app.register_blueprint(main_routes)
    app.register_blueprint(api_routes, url_prefix='/api')
    return app


if __name__ == '__main__':
    app = create_app('development')
    app.run()
