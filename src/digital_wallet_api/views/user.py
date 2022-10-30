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
