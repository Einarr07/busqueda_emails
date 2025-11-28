from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.common import IsActiveEnum


class ClientBase(BaseModel):
    name = str
    is_active = IsActiveEnum = IsActiveEnum.ACTIVE


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name = Optional[str] = None
    is_active = Optional[IsActiveEnum] = None


class ClientRead(ClientBase):
    id_client = int
    created_at: datetime

    class Config:
        orm_mode = True

    model_config = {'from_attributes': True}
