from sqlalchemy.orm import Session

from .. import models, schemas


def get_user_by_id(db: Session, user_id: id):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_pin = user.pin
    db_user = models.User(name=user.name, pin=hashed_pin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
