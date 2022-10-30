from digital_wallet_api import repository, schemas
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .utils import (
    convert_taka_to_paisha,
    convert_transaction_to_use_taka,
    check_if_user_exists,
    verify_pin_requirements,
)


def signup(user: schemas.UserCreate, db: Session):
    if not verify_pin_requirements(user.pin):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Pin has to be 5 digits"
        )
    db_user = repository.user.create_user(db=db, user=user)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registerd."
        )
    return db_user


def transfer(user_id, transfer_request: schemas.TransferRequest, db: Session):
    from_user_id = user_id
    check_if_user_exists(user_id=from_user_id, db=db)
    to_user_id = transfer_request.to_user_id
    check_if_user_exists(user_id=to_user_id, db=db)
    amount_in_taka = transfer_request.amount

    amount_in_paisa = convert_taka_to_paisha(amount_in_taka)

    transaction = repository.user.transfer_amount(
        db=db, from_user_id=from_user_id, to_user_id=to_user_id, amount=amount_in_paisa
    )
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Low balance on sender account.",
        )

    return convert_transaction_to_use_taka(transaction)


def get_transactions(user_id: int, db: Session):
    check_if_user_exists(user_id=user_id, db=db)
    transactions = repository.transaction.get_user_transactions(db=db, user_id=user_id)
    transactions_converted = list(map(convert_transaction_to_use_taka, transactions))
    return schemas.Transactions(transactions=transactions_converted)
