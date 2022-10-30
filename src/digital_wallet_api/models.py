from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), index=True)
    pin = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
