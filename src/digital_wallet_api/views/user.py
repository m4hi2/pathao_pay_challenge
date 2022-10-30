from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from digital_wallet_api import schemas, repository


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


def verify_pin_requirements(pin: str) -> bool:
    """According to the requirements, the pin has to be 5 digits.

    Args:
        pin (str): User provided pin

    Returns:
        bool: Wheather the pin meets requirements or not.
    """

    if len(pin) != 5:
        return False

    try:
        int(pin)
    except ValueError:
        return False

    return True


def transfer(user_id, transfer_request: schemas.TransferRequest, db: Session):
    from_user_id = user_id
    to_user_id = transfer_request.to_user_id
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
    transactions = repository.transaction.get_user_transactions(db=db, user_id=user_id)
    transactions_converted = list(map(convert_transaction_to_use_taka, transactions))
    return schemas.Transactions(transactions=transactions_converted)


def convert_transaction_to_use_taka(
    transaction: schemas.TransactionCreate,
) -> schemas.Transaction:
    converted_transaction = schemas.Transaction(
        transaction_date=transaction.transaction_date,
        transaction_id=transaction.transaction_id,
        from_user_id=transaction.from_user_id,
        to_user_id=transaction.to_user_id,
        amount=convert_paisa_to_taka(transaction.amount),
    )

    return converted_transaction


def convert_taka_to_paisha(amount: float) -> int:
    paisa_amount = amount * 100
    try:
        paisa_amount = int(paisa_amount)
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Only 2 decimal digit allowed for transfer amount"
        )

    return paisa_amount


def convert_paisa_to_taka(amount: int) -> float:
    taka_amount = amount / 100

    return taka_amount
