from decimal import Decimal

import pytest

from app import create_app
from app.config import TestingConfig
from app.extensions import db
from app.models import Account, User


@pytest.fixture
def app():
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()

        alice = User(
            full_name="Alice Johnson",
            email="alice.test@example.com",
            role="customer",
        )

        bob = User(
            full_name="Bob Smith",
            email="bob.test@example.com",
            role="customer",
        )

        db.session.add_all([alice, bob])
        db.session.flush()

        alice_account = Account(
            account_number="TEST-100001",
            account_type="savings",
            balance=Decimal("5000.00"),
            currency="GBP",
            user_id=alice.id,
        )

        bob_account = Account(
            account_number="TEST-100002",
            account_type="current",
            balance=Decimal("3200.00"),
            currency="GBP",
            user_id=bob.id,
        )

        db.session.add_all([alice_account, bob_account])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
