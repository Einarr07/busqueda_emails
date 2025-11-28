from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Email, Company
from app.schemas import EmailRead, EmailBulkCreate, EmailSearchResponse, EmailSearchFilters

router = APIRouter(
    prefix="/client/{client_id}/emails",
    tags=["email"],
    responses={404: {"description": "Not found"}},
)


@router.post('/', response_model=List[EmailRead], status_code=status.HTTP_201_CREATED)
def bulk_create_emails(
        client_id: int,
        payload: EmailBulkCreate,
        db: Session = Depends(get_db)
):
    if not payload.emails:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No emails for registers"
        )

    emails_to_create: List[Email] = []

    for email_data in payload.emails:
        # Encontrar empresa por nombre y cliente
        query_company = select(Company).where(
            Company.client_id == client_id,
            Company.name == email_data.company_name
        )
        company = db.execute(query_company).scalars().first()

        if company is None:
            # Empresa no parametrizada -> no guarda
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f'Company {email_data.company_name} is not parametrized'
                    f' for client {client_id}'
                )
            )
        email = Email(
            client_id=client_id,
            company_id=company.id_company,
            sender=email_data.sender,
            recipient=email_data.recipient,
            sent_at=email_data.sent_at,
            smtp_provider=email_data.smtp_provider,  # once_code
            smtp_message_id=email_data.smtp_message_id,
            subject=email_data.subject,
            content=email_data.content,
        )

        emails_to_create.append(email)

    db.add_all(emails_to_create)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f'1 or more emails violate a uniqueness restriction'
                f'(smtp_provider, smtp_message_id)'
            )
        )

    for email in emails_to_create:
        db.refresh(email)

    return emails_to_create


@router.get('/', response_model=EmailSearchResponse, status_code=status.HTTP_200_OK)
async def search_emails(
        client_id: int,
        filters: EmailSearchFilters = Depends(EmailSearchFilters),
        db: Session = Depends(get_db)
):
    # Si no existe filtro -> list[]
    if not any(
            [
                filters.content,
                filters.sender,
                filters.recipient,
                filters.company_id,
                filters.from_date,
                filters.to_date
            ]
    ):
        return EmailSearchResponse(
            items=[],
            total=0,
            page=filters.page,
            page_size=filters.page_size,
        )

    query = select(Email).where(Email.client_id == client_id)

    if filters.content:
        query = query.where(Email.content.ilike(f'%{filters.content}%'))

    if filters.sender:
        query = query.where(Email.sender == filters.sender)

    if filters.recipient:
        query = query.where(Email.recipient == filters.recipient)

    if filters.company_id:
        query = query.where(Email.client_id == client_id)

    if filters.from_date:
        query = query.where(Email.sent_at >= filters.from_date)

    if filters.to_date:
        query = query.where(Email.sent_at <= filters.to_date)

    # Total de resultados
    count_query = select(func.count()).select_from(query.subquery())
    total = db.execute(count_query).scalar_one()

    # Paginación

    offset = (filters.page - 1) * filters.page_size
    query = query.offset(offset).limit(filters.page_size)

    result = db.execute(query)
    emails = result.scalars().all()

    return EmailSearchResponse(
        items=emails,
        total=total,
        page=filters.page,
        page_size=filters.page_size,
    )
