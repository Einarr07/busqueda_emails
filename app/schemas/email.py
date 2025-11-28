from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class EmailBase(BaseModel):
    sender: str
    recipient: str
    sent_at: datetime

    smtp_provider: str
    smtp_message_id: str

    subject: Optional[str] = None
    content: str


class EmailCreate(EmailBase):
    company_name: str


class EmailBulkCreate(BaseModel):
    emails: List[EmailCreate]


class EmailRead(EmailBase):
    id_email: int
    client_id: int
    company_id: int
    created_at: datetime

    class Config:
        orm_mode = True

    model_config = {'from_attributes': True}


class EmailSearchFilters(BaseModel):
    content: str
    sender: Optional[str] = None
    recipient: Optional[str] = None
    company_id: Optional[int] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None

    page: int = 1
    page_size: int = 20


class EmailSearchResponse(BaseModel):
    items: List[EmailRead]
    total: int
    page: int
    page_size: int
