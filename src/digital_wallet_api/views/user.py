from digital_wallet_api import repository, schemas
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .utils import (
    check_if_user_exists,
    convert_taka_to_paisha,
    convert_transaction_to_use_taka,
    verify_pin_requirements,
)


def signup(user: schemas.UserCreate, db: Session):
    """Creates a new user with wallet and initial balalnce of 5000

    Args:
        user (schemas.UserCreate): User creation info
        db (Session): database connection

    Raises:
        HTTPException: Pin invalid
        HTTPException: Email already registed.

    Returns:
        user (schemas.User): created user
    """
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


def transfer(user_id: int, transfer_request: schemas.TransferRequest, db: Session):
    """Transfers balance from a users wallet to another users wallet.

    Args:
        user_id (int): userID of the from user
        transfer_request (schemas.TransferRequest): transfer details - ammount and to user
        db (Session): database connection

    Raises:
        HTTPException: Low balance | User doesn't exists

    Returns:
        transaction (schemas.Transaction): the transaction details
    """
    from_user_id = user_id
    check_if_user_exists(user_id=from_user_id, db=db)
    to_user_id = transfer_request.to_user_id
    check_if_user_exists(user_id=to_user_id, db=db)

    if from_user_id == to_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sender and reciver can not be same.",
        )
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
    """Gets the transation lisf for the given userID

    Args:
        user_id (int): userID of the user
        db (Session): database connection

    Returns:
        transactions (schemas.Transactions): list of the user's transactions.
    """
    check_if_user_exists(user_id=user_id, db=db)
    transactions = repository.transaction.get_user_transactions(db=db, user_id=user_id)
    transactions_converted = list(map(convert_transaction_to_use_taka, transactions))
    return schemas.Transactions(transactions=transactions_converted)


def get_user_balance(user_email: str, db: Session):
    return repository.user.get_user_balance(db=db, user_email=user_email)
