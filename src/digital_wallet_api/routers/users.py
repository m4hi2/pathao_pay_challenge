from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from digital_wallet_api import schemas, repository
from digital_wallet_api.database import get_db


router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return repository.user.create_user(db, user=user)
