from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    pin: str


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class WalletBase(BaseModel):
    balance: float


class Wallet(WalletBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
