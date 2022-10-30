from sqlalchemy.orm import Session

from digital_wallet_api import models, schemas


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
    return db_user
