from datetime import datetime, timezone

from app.extensions import db


class AuditEvent(db.Model):
    __tablename__ = "audit_events"

    id = db.Column(db.Integer, primary_key=True)

    event_type = db.Column(db.String(80), nullable=False, index=True)
    actor = db.Column(db.String(180), nullable=True)
    entity_type = db.Column(db.String(80), nullable=True)
    entity_id = db.Column(db.String(80), nullable=True)

    outcome = db.Column(db.String(30), nullable=False, default="success")
    ip_address = db.Column(db.String(45), nullable=True)

    # JSON works with SQLite and PostgreSQL.
    metadata_json = db.Column(db.JSON, nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
