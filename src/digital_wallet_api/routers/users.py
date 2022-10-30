from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from digital_wallet_api import schemas, repository
from digital_wallet_api.database import get_db


router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = repository.user.create_user(db=db, user=user)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registerd."
        )
    return db_user
