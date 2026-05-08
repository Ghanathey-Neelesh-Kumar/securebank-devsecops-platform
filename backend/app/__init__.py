from flask import Flask

from app.config import get_config
from app.extensions import cors, db, migrate
from app.routes.health import health_bp


def create_app(config_object=None):
    app = Flask(__name__)

    if config_object:
        app.config.from_object(config_object)
    else:
        app.config.from_object(get_config())

    cors.init_app(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:8081",
                    "http://127.0.0.1:8081",
                    "http://localhost:8080",
                    "http://127.0.0.1:8080",
                    "http://localhost:5500",
                    "http://127.0.0.1:5500",
                    "http://localhost:3000",
                    "http://127.0.0.1:3000",
                ]
            }
        },
    )

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models  # noqa: F401

    from app.commands.seed import seed_db
    from app.routes.api import api_bp

    app.cli.add_command(seed_db)

    app.register_blueprint(health_bp)
    app.register_blueprint(api_bp)

    return app
