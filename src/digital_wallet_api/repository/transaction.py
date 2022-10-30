from uuid import uuid4
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
