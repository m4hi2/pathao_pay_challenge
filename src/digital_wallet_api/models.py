from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    hashed_pin = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    wallet = relationship("Wallet", back_populates="user", uselist=False)


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    # balance is kept as "paisa" instead of taka, to prevent
    # rounding/foating point airethmatic errors.
    balance = Column(Integer, default=500000)
    user = relationship("User", back_populates="wallet")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_date = Column(DateTime(timezone=True), default=datetime.utcnow)
    from_user_id = Column(Integer, index=True)
    to_user_id = Column(Integer, index=True)
    # ammount is kept as "paisa" instead of taka, to prevent
    # rounding/foating point airethmatic errors.
    ammount = Column(Integer)
