from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Float

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    hashed_pin = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    balance = Column(Float, default=5000)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_date = Column(DateTime(timezone=True), default=datetime.utcnow)
    from_user_id = Column(Integer, index=True)
    to_user_id = Column(Integer, index=True)
    ammount = Column(Float)
