from flask import Flask

from app.config import get_config
from app.extensions import cors
from app.routes.health import health_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    cors.init_app(app)

    app.register_blueprint(health_bp)

    return app
