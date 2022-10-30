from digital_wallet_api import repository, schemas
from sqlalchemy.orm import Session

from .utils import convert_paisa_to_taka


def get_system_balance(db: Session):
    system_balance = repository.wallet.get_all_wallet_balance_sum(db)
    system_balance_in_taka = convert_paisa_to_taka(system_balance)
    return schemas.SystemBalance(balance=system_balance_in_taka)
