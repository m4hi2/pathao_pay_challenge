from sqlalchemy.orm import Session

from digital_wallet_api import models, schemas
from .wallet import (
    add_amount_to_wallet,
    charge_wallet,
    create_wallet,
)


def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    if get_user_by_email(db, user.email):
        return None

    hased_pin = user.pin
    db_user = models.User(email=user.email, name=user.name, pin=hased_pin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    create_wallet(db=db, user_id=db_user.id)
    return db_user


def get_user_wallet(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first().wallet[0]


def transfer_amount(
    db: Session, from_user_id: int, to_user_id: int, amount: int
) -> bool:
    from_user_wallet = get_user_wallet(db, from_user_id)
    if not charge_wallet(db, from_user_wallet, amount):
        return False
    to_user_wallet = get_user_wallet(db, to_user_id)
    add_amount_to_wallet(db, to_user_wallet, amount)
    return True
