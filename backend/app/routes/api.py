from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import Account, AuditEvent, Transaction
from app.services.transfer_service import TransferError, transfer_money

api_bp = Blueprint("api", __name__, url_prefix="/api")


def serialize_account(account):
    return {
        "id": account.id,
        "account_number": account.account_number,
        "account_type": account.account_type,
        "balance": str(account.balance),
        "currency": account.currency,
        "status": account.status,
        "user": {
            "id": account.user.id,
            "full_name": account.user.full_name,
            "email": account.user.email,
        },
        "created_at": account.created_at.isoformat() if account.created_at else None,
    }


def serialize_transaction(transaction):
    return {
        "id": transaction.id,
        "from_account_id": transaction.from_account_id,
        "to_account_id": transaction.to_account_id,
        "amount": str(transaction.amount),
        "currency": transaction.currency,
        "status": transaction.status,
        "reference": transaction.reference,
        "created_at": transaction.created_at.isoformat()
        if transaction.created_at
        else None,
    }


def serialize_audit_event(event):
    return {
        "id": event.id,
        "event_type": event.event_type,
        "actor": event.actor,
        "entity_type": event.entity_type,
        "entity_id": event.entity_id,
        "outcome": event.outcome,
        "ip_address": event.ip_address,
        "metadata": event.metadata_json,
        "created_at": event.created_at.isoformat() if event.created_at else None,
    }


@api_bp.get("/accounts")
def get_accounts():
    accounts = Account.query.order_by(Account.id.asc()).all()

    return jsonify(
        {
            "count": len(accounts),
            "accounts": [serialize_account(account) for account in accounts],
        }
    ), 200


@api_bp.get("/accounts/<int:account_id>")
def get_account(account_id):
    account = Account.query.get(account_id)

    if not account:
        return jsonify({"error": "Account not found"}), 404

    return jsonify(serialize_account(account)), 200


@api_bp.get("/transactions")
def get_transactions():
    transactions = Transaction.query.order_by(Transaction.created_at.desc()).all()

    return jsonify(
        {
            "count": len(transactions),
            "transactions": [
                serialize_transaction(transaction) for transaction in transactions
            ],
        }
    ), 200


@api_bp.get("/audit-events")
def get_audit_events():
    events = AuditEvent.query.order_by(AuditEvent.created_at.desc()).all()

    return jsonify(
        {
            "count": len(events),
            "audit_events": [serialize_audit_event(event) for event in events],
        }
    ), 200


@api_bp.post("/transfer")
def create_transfer():
    data = request.get_json(silent=True) or {}

    required_fields = ["from_account_id", "to_account_id", "amount"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify(
            {
                "error": "Missing required fields",
                "missing_fields": missing_fields,
            }
        ), 400

    try:
        transaction = transfer_money(
            from_account_id=data["from_account_id"],
            to_account_id=data["to_account_id"],
            amount_value=data["amount"],
            actor=data.get("actor", "api-user"),
            ip_address=request.headers.get("X-Forwarded-For", request.remote_addr),
        )

        db.session.commit()

        return jsonify(
            {
                "message": "Transfer completed successfully",
                "transaction": serialize_transaction(transaction),
            }
        ), 201

    except TransferError as error:
        db.session.rollback()

        return jsonify(
            {
                "error": str(error),
            }
        ), 400

    except Exception:
        db.session.rollback()

        return jsonify(
            {
                "error": "Unexpected error while processing transfer",
            }
        ), 500
