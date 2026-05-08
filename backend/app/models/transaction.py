from datetime import datetime, timezone
from decimal import Decimal

from app.extensions import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    from_account_id = db.Column(
        db.Integer,
        db.ForeignKey("accounts.id"),
        nullable=False,
    )
    to_account_id = db.Column(
        db.Integer,
        db.ForeignKey("accounts.id"),
        nullable=False,
    )

    amount = db.Column(db.Numeric(12, 2), nullable=False, default=Decimal("0.00"))
    currency = db.Column(db.String(3), nullable=False, default="GBP")

    status = db.Column(db.String(30), nullable=False, default="completed")
    reference = db.Column(db.String(100), nullable=False, unique=True, index=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    from_account = db.relationship(
        "Account",
        foreign_keys=[from_account_id],
        back_populates="outgoing_transactions",
    )

    to_account = db.relationship(
        "Account",
        foreign_keys=[to_account_id],
        back_populates="incoming_transactions",
    )
