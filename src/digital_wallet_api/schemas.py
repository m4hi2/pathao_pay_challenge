from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    pin: str


class User(UserBase):
    id: int
    created_at: datetime
    balance: float

    class Config:
        orm_mode = True


class Transaction(BaseModel):
    id: int
    transaction_date: datetime
    from_user_id: int
    to_user_id: int
    amount: float

    class Config:
        orm_mode = True
