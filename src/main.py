from fastapi import FastAPI
from digital_wallet_api import models
from digital_wallet_api.database import engine
from digital_wallet_api.routers import users, system, authentication

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(users.router)
app.include_router(system.router)
app.include_router(authentication.router)
