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


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    is_active: Optional[IsActiveEnum] = None


class CompanyRead(CompanyBase):
    id_company: int
    client_id: int
    created_at: datetime

    model_config = {'from_attributes': True}
