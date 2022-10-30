from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from digital_wallet_api import schemas, views
from digital_wallet_api.database import get_db


router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return views.user.signup(user=user, db=db)


@router.post("/{id}/transfer", response_model=schemas.Transaction)
def transfer_balance(
    id: int, transfer_request: schemas.TransferRequest, db: Session = Depends(get_db)
):
    return views.user.transfer(user_id=id, transfer_request=transfer_request, db=db)


@router.get("/{id}/transactions", response_model=schemas.Transactions)
def get_user_transactions(id: int, db: Session = Depends(get_db)):
    return views.user.get_transactions(user_id=id, db=db)
