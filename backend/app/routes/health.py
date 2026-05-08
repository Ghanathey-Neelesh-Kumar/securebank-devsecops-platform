from datetime import datetime, timezone

from flask import Blueprint, current_app, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "service": current_app.config["APP_NAME"],
            "version": current_app.config["APP_VERSION"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    ), 200


@health_bp.get("/ready")
def ready():
    return jsonify(
        {
            "status": "ready",
            "service": current_app.config["APP_NAME"],
            "version": current_app.config["APP_VERSION"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    ), 200
