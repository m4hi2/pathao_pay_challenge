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


def get_wallet_by_user_id(db: Session, user_id: int):
    db_wallet = db.query(models.Wallet).filter(models.Wallet.user_id == user_id).first()
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
