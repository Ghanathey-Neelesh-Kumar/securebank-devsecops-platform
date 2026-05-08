from decimal import Decimal, InvalidOperation
from uuid import uuid4

from app.extensions import db
from app.models import Account, AuditEvent, Transaction


class TransferError(Exception):
    """Raised when a transfer cannot be completed."""


def parse_amount(value):
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError):
        raise TransferError("Invalid transfer amount")

    if amount <= Decimal("0.00"):
        raise TransferError("Transfer amount must be greater than zero")

    return amount.quantize(Decimal("0.01"))


def create_audit_event(
    event_type,
    outcome,
    actor=None,
    entity_type=None,
    entity_id=None,
    ip_address=None,
    metadata=None,
):
    audit_event = AuditEvent(
        event_type=event_type,
        actor=actor,
        entity_type=entity_type,
        entity_id=entity_id,
        outcome=outcome,
        ip_address=ip_address,
        metadata_json=metadata or {},
    )

    db.session.add(audit_event)
    return audit_event


def transfer_money(
    from_account_id,
    to_account_id,
    amount_value,
    actor="system",
    ip_address=None,
):
    amount = parse_amount(amount_value)

    if from_account_id == to_account_id:
        raise TransferError("Source and destination accounts must be different")

    from_account = Account.query.filter_by(id=from_account_id).with_for_update().first()
    to_account = Account.query.filter_by(id=to_account_id).with_for_update().first()

    if not from_account or not to_account:
        create_audit_event(
            event_type="transfer.failed",
            outcome="failure",
            actor=actor,
            entity_type="transaction",
            ip_address=ip_address,
            metadata={
                "reason": "Invalid account details",
                "from_account_id": from_account_id,
                "to_account_id": to_account_id,
                "amount": str(amount),
            },
        )
        raise TransferError("Invalid account details")

    if from_account.status != "active" or to_account.status != "active":
        create_audit_event(
            event_type="transfer.failed",
            outcome="failure",
            actor=actor,
            entity_type="transaction",
            ip_address=ip_address,
            metadata={
                "reason": "One or more accounts are not active",
                "from_account_id": from_account_id,
                "to_account_id": to_account_id,
                "amount": str(amount),
            },
        )
        raise TransferError("One or more accounts are not active")

    if from_account.currency != to_account.currency:
        create_audit_event(
            event_type="transfer.failed",
            outcome="failure",
            actor=actor,
            entity_type="transaction",
            ip_address=ip_address,
            metadata={
                "reason": "Currency mismatch",
                "from_currency": from_account.currency,
                "to_currency": to_account.currency,
            },
        )
        raise TransferError("Currency mismatch between accounts")

    if from_account.balance < amount:
        create_audit_event(
            event_type="transfer.failed",
            outcome="failure",
            actor=actor,
            entity_type="transaction",
            ip_address=ip_address,
            metadata={
                "reason": "Insufficient balance",
                "from_account_id": from_account.id,
                "available_balance": str(from_account.balance),
                "requested_amount": str(amount),
            },
        )
        raise TransferError("Insufficient balance")

    reference = f"SB-{uuid4().hex[:12].upper()}"

    from_account.balance -= amount
    to_account.balance += amount

    transaction = Transaction(
        from_account_id=from_account.id,
        to_account_id=to_account.id,
        amount=amount,
        currency=from_account.currency,
        status="completed",
        reference=reference,
    )

    db.session.add(transaction)
    db.session.flush()

    create_audit_event(
        event_type="transfer.completed",
        outcome="success",
        actor=actor,
        entity_type="transaction",
        entity_id=str(transaction.id),
        ip_address=ip_address,
        metadata={
            "reference": reference,
            "from_account_id": from_account.id,
            "to_account_id": to_account.id,
            "amount": str(amount),
            "currency": from_account.currency,
        },
    )

    return transaction
