import os


class Config:
    APP_NAME = os.getenv("APP_NAME", "securebank-api")
    APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    FLASK_ENV = os.getenv("FLASK_ENV", "production")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///securebank.db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    TESTING = False
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS = {}


def get_config():
    env = os.getenv("FLASK_ENV", "production").lower()

    if env == "development":
        return DevelopmentConfig

    if env == "testing":
        return TestingConfig

    return ProductionConfig
