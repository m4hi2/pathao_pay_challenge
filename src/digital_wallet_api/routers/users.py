from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from digital_wallet_api import schemas, views
from digital_wallet_api.database import get_db
from digital_wallet_api.auth.oauth2 import get_current_user

router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """New user sign up.
    Creates user and a wallet for the user with 5000 taka initial balance.
    """
    return views.user.signup(user=user, db=db)


@router.post("/{id}/transfer", response_model=schemas.Transaction)
def transfer_balance(
    id: int, transfer_request: schemas.TransferRequest, db: Session = Depends(get_db)
):
    """Transfers balance from User{id} to another user. The receiving user and amount can
    be sent through request body.
    If transfer is successful, returns the transaction.
    """
    return views.user.transfer(user_id=id, transfer_request=transfer_request, db=db)


@router.get("/{id}/transactions", response_model=schemas.Transactions)
def get_user_transactions(id: int, db: Session = Depends(get_db)):
    """Returns a list of transactions that is related to the User{id}"""
    return views.user.get_transactions(user_id=id, db=db)


@router.get("/me/balance", response_model=schemas.UserBalance)
def get_user_balance(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """Get balance of authorized user."""
    return views.user.get_user_balance(user_email=current_user.email, db=db)
