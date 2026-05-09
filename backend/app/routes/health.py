from datetime import datetime, timezone

from flask import Blueprint, current_app, jsonify
from sqlalchemy import text

from app.extensions import db

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
    checks = {
        "database": "unknown",
    }

    try:
        db.session.execute(text("SELECT 1"))
        checks["database"] = "ready"

        return jsonify(
            {
                "status": "ready",
                "service": current_app.config["APP_NAME"],
                "version": current_app.config["APP_VERSION"],
                "checks": checks,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ), 200

    except Exception as error:
        checks["database"] = "unavailable"

        return jsonify(
            {
                "status": "not_ready",
                "service": current_app.config["APP_NAME"],
                "version": current_app.config["APP_VERSION"],
                "checks": checks,
                "error": str(error),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ), 503
