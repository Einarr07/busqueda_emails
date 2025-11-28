from fastapi import FastAPI
from starlette.responses import RedirectResponse

import app.models
from app.db import engine, Base
from .routers import client, company, email

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title='Fraud Email API',
    responses={404: {"description": "Not found"}},
)

app.include_router(client.router, prefix='/api')
app.include_router(company.router, prefix="/api")
app.include_router(email.router, prefix="/api")


@app.get('/')
def main():
    return RedirectResponse(url="/docs")
