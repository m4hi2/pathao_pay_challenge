from sqlalchemy.orm import Session

from .. import models, schemas


def get_user_by_id(db: Session, user_id: id):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    if not check_pin_size(user.pin):
        return None
    hashed_pin = user.pin
    db_user = models.User(name=user.name, hashed_pin=hashed_pin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_pin_size(pin: str) -> bool:
    """The requirement is that pin is of 5 digits.

    Args:
        pin (str): user pin

    Returns:
        bool: if the pin size is 5 or not and if is digits.
    """
    if len(pin) != 5:
        return False
    try:
        int(pin)
    except ValueError:
        return False
    return True
