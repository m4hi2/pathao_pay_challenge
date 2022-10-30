from sqlalchemy.orm import Session

from digital_wallet_api import models


def create_wallet(db: Session, user_id: int):
    """Creates wallet with initial balance of 5000 for
    the user

    Args:
        db (Session): Database Session
        user_id (int): User ID for whom the wallet will be created.
    """
    db_wallet = models.Wallet(user_id=user_id)
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet


def charge_wallet(db: Session, wallet: models.Wallet, amount: int):
    if amount > wallet.balance:
        return None

    wallet.balance = wallet.balance - amount

    db.commit()
    db.refresh(wallet)
    return wallet


def add_amount_to_wallet(db: Session, wallet: models.Wallet, amount: int):
    wallet.balance = wallet.balance + amount

    db.commit()
    db.refresh(wallet)
    return wallet


def get_all_wallet_balance_sum(db: Session) -> int:
    sum = 0
    wallets = db.query(models.Wallet).all()
    for wallet in wallets:
        sum += wallet.balance

    return sum
