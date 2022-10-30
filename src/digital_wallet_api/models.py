from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), index=True, unique=True)
    pin = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    wallet = relationship(
        "Wallet",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    # keeping balance as paisa to prevent rounding error and
    # floating point arithmetics.
    balance = Column(Integer, default=500000)
    type = Column(String, default="bdt_paisa")

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADe"))
    user = relationship(
        "User",
        back_populates="wallet",
    )
