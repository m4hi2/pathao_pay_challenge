from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from digital_wallet_api import schemas, repository
from digital_wallet_api.database import get_db


router = APIRouter(tags=["Users"], prefix="/users")
