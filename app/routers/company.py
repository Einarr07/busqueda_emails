from typing import List, Optional

from fastapi import APIRouter, status, Depends, Query, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.schemas import CompanyRead, CompanyCreate
from ..db import get_db
from ..models import Company
from ..schemas.company import CompanyUpdate

router = APIRouter(
    prefix="/company",
    tags=["Company"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[CompanyRead], status_code=status.HTTP_200_OK)
async def list_companies(
        client_id: Optional[int] = Query(None, description='Filter by client_id'),
        db: Session = Depends(get_db)
):
    query = select(Company)
    if client_id is not None:
        query = query.where(Company.client_id == client_id)

    result = db.execute(query)
    companies = result.scalars().all()
    return companies


@router.get('/{company_id}', response_model=CompanyRead, status_code=status.HTTP_200_OK)
async def get_company(company_id: int, db: Session = Depends(get_db)):
    company_db = db.get(Company, company_id)
    if not company_db:
        raise HTTPException(status_code=404, detail="Company not found")
    return company_db


@router.post('/', response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
async def create_company(company_data: CompanyCreate, db: Session = Depends(get_db)):
    company = Company(**company_data.model_dump())
    db.add(company)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="There is already a company with that name for this client."
        )
    except Exception as err:
        db.rollback()
        raise f'Error: {err}'

    db.refresh(company)
    return company


@router.put('/{company_id}', response_model=CompanyRead, status_code=status.HTTP_200_OK)
async def update_company(
        company_id: int,
        company_data: CompanyUpdate,
        db: Session = Depends(get_db),
):
    company_db = db.get(Company, company_id)
    if not company_db:
        raise HTTPException(status_code=404, detail="Company not found")

    update_data = company_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company_db, field, value)

    db.commit()
    db.refresh(company_db)
    return company_db


@router.delete('/{company_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: int, db: Session = Depends(get_db)):
    company_db = db.get(Company, company_id)
    if not company_db:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(company_db)
    db.commit()
