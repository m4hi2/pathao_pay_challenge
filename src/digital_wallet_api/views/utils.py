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
    """The transactions in db have amount in paisa. But we need
    to show them in taka. This function convert the paisa value
    to taka when creating the response model.

    Args:
        transaction (schemas.TransactionCreate): The transaction to be converted

    Returns:
        schemas.Transaction: Converted transaction
    """
    converted_transaction = schemas.Transaction(
        transaction_date=transaction.transaction_date,
        transaction_id=transaction.transaction_id,
        from_user_id=transaction.from_user_id,
        to_user_id=transaction.to_user_id,
        amount=convert_paisa_to_taka(transaction.amount),
    )

    return converted_transaction


def convert_taka_to_paisha(amount: float) -> int:
    """Converts taka value to paisa

    Args:
        amount (float): amount in taka

    Raises:
        HTTPException: supports only 2 decimal digit

    Returns:
        int: paisa amount
    """
    paisa_amount = amount * 100
    try:
        paisa_amount = int(paisa_amount)
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Only 2 decimal digit allowed for transfer amount"
        )

    return paisa_amount


def convert_paisa_to_taka(amount: int) -> float:
    """Converts paisa value to taka

    Args:
        amount (int): amount in paisa

    Returns:
        taka_amount (float): amount in taka
    """
    taka_amount = amount / 100

    return taka_amount


def check_if_user_exists(user_id: int, db: Session):
    if not repository.user.get_user_by_id(db=db, id=user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"UserID {user_id} doesn't exists ",
        )
