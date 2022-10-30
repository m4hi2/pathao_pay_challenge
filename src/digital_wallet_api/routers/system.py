from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from digital_wallet_api import schemas, views
from digital_wallet_api.database import get_db


router = APIRouter(tags=["System"], prefix="/system")


@router.get("/", response_model=schemas.SystemBalance)
def get_system_balance(db: Session = Depends(get_db)):
    """Gets the total system balance. Balance of all walltes summed."""
    return views.wallet.get_system_balance(db=db)
