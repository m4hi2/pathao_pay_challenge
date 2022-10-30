from uuid import uuid4
from sqlalchemy import or_, desc
from sqlalchemy.orm import Session

from digital_wallet_api import models, schemas


def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(
        transaction_id=str(uuid4()),
        amount=transaction.amount,
        from_user_id=transaction.from_user_id,
        to_user_id=transaction.to_user_id,
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_user_transactions(db: Session, user_id: int):
    transactions = (
        db.query(models.Transaction)
        .filter(
            or_(
                models.Transaction.from_user_id == user_id,
                models.Transaction.to_user_id == user_id,
            )
        )
        .order_by(desc(models.Transaction.transaction_date))
        .all()
    )
    return transactions
