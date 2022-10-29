from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from digital_wallet_api import schemas, repository
from digital_wallet_api.database import get_db


router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = repository.user.create_user(db, user=user)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Pin must be of 5 digits"
        )
    return db_user


@router.get("/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = repository.user.get_user_by_id(db, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not found"
        )
    return user
