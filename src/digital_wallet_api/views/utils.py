from digital_wallet_api import repository, schemas
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


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


def get_user_or_raise(user_id: int, db: Session):
    if not repository.user.get_user_by_id(db=db, id=user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"UserID {user_id} doesn't exists ",
        )
