from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.common import IsActiveEnum


class CompanyBase(BaseModel):
    name: str
    domain: Optional[str] = None
    is_active: IsActiveEnum = IsActiveEnum.ACTIVE


class CompanyCreate(CompanyBase):
    client_id: int


class CompanyRead(CompanyBase):
    client_id: int


class CompanyUpdate(CompanyBase):
    id_company: int
    client_id: int
    created_at: datetime

    class Config:
        orm_mode = True

    model_config = {'from_attributes': True}
