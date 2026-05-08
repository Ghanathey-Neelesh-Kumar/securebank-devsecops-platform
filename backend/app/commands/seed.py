from decimal import Decimal

import click
from flask.cli import with_appcontext

from app.extensions import db
from app.models import Account, AuditEvent, User


@click.command("seed-db")
@with_appcontext
def seed_db():
    """Seed the database with initial SecureBank data."""

    existing_user = User.query.filter_by(email="alice.securebank@example.com").first()

    if existing_user:
        click.echo("Seed data already exists. Skipping.")
        return

    alice = User(
        full_name="Alice Johnson",
        email="alice.securebank@example.com",
        role="customer",
    )

    bob = User(
        full_name="Bob Smith",
        email="bob.securebank@example.com",
        role="customer",
    )

    db.session.add_all([alice, bob])
    db.session.flush()

    alice_account = Account(
        account_number="SB-100001",
        account_type="savings",
        balance=Decimal("5000.00"),
        currency="GBP",
        user_id=alice.id,
    )

    bob_account = Account(
        account_number="SB-100002",
        account_type="current",
        balance=Decimal("3200.00"),
        currency="GBP",
        user_id=bob.id,
    )

    audit_event = AuditEvent(
        event_type="database.seed",
        actor="system",
        entity_type="database",
        entity_id="initial-seed",
        outcome="success",
        metadata_json={
            "message": "Initial SecureBank demo users and accounts created",
            "users": 2,
            "accounts": 2,
        },
    )

    db.session.add_all([alice_account, bob_account, audit_event])
    db.session.commit()

    click.echo("Seed data created successfully.")
