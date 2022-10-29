from datetime import datetime
from email.policy import default

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    hashed_pin = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    # balance is kept as "paisa" instead of taka, to prevent
    # rounding/foating point airethmatic errors.
    balance = Column(Integer, default=500000)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_date = Column(DateTime(timezone=True), default=datetime.utcnow)
    from_user_id = Column(Integer, index=True)
    to_user_id = Column(Integer, index=True)
    # ammount is kept as "paisa" instead of taka, to prevent
    # rounding/foating point airethmatic errors.
    ammount = Column(Integer)
