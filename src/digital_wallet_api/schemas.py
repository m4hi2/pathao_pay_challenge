from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    pin: str


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TransferRequest(BaseModel):
    to_user_id: int
    amount: float


class Transaction(BaseModel):
    transaction_date: datetime
    transation_id: str
    from_user_id: int
    to_user_id: int
    amount: float
