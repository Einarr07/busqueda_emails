from typing import List

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas import ClientRead, ClientCreate, ClientUpdate
from ..db import get_db
from ..models.clients import Client

router = APIRouter(
    prefix="/client",
    tags=["client"],
    responses={404: {"description": "Not found"}},
)


@router.get('/', response_model=List[ClientRead], status_code=status.HTTP_200_OK)
async def list_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()


@router.get('/{id}', response_model=ClientRead, status_code=status.HTTP_200_OK)
async def get_client(id: int, db: Session = Depends(get_db)):
    client_db = db.get(Client, id)
    if not client_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return client_db


@router.post('/', response_model=ClientRead, status_code=status.HTTP_201_CREATED)
async def create_client(client_data: ClientCreate, db: Session = Depends(get_db)):
    client = Client(**client_data.model_dump())

    db.add(client)
    db.commit()
    db.refresh(client)
    
    return client


@router.put('/{id}', response_model=ClientRead, status_code=status.HTTP_200_OK)
async def update_client(
        id: int,
        client_data: ClientUpdate,
        db: Session = Depends(get_db)
):
    client_db = db.get(Client, id)

    if not client_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    update_data = client_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(client_db, field, value)

    db.commit()
    db.refresh(client_db)
    return client_db


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(id: int, db: Session = Depends(get_db)):
    client_db = db.get(Client, id)
    if not client_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    db.delete(client_db)
    db.commit()
