from datetime import datetime
from pydantic import BaseModel
from typing import Optional


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


class UserBalance(BaseModel):
    balance: float
    user_email: str

    class Config:
        orm_mode = True


class TransferRequest(BaseModel):
    to_user_id: int
    amount: float


class TransactionBase(BaseModel):
    from_user_id: int
    to_user_id: int
    amount: float


class TransactionCreate(TransactionBase):
    amount: int


class Transaction(TransactionBase):
    transaction_id: str
    transaction_date: datetime

    class Config:
        orm_mode = True


class Transactions(BaseModel):
    transactions: list[Transaction]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class SystemBalance(BaseModel):
    balance: float

    class Config:
        orm_mode = True
