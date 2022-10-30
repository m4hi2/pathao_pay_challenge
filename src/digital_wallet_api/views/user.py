from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from digital_wallet_api import schemas, repository


def signup(user: schemas.UserCreate, db: Session):
    db_user = repository.user.create_user(db=db, user=user)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registerd."
        )
    return db_user
