from sqlalchemy import Column, DateTime, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .common import IsActiveEnum
from ..db import Base


class Client(Base):
    __tablename__ = 'clients'

    id_client = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(60), nullable=False)
    is_active = Column(
        Enum(IsActiveEnum, name='client_is_active_enum'),
        nullable=False,
        default=IsActiveEnum.ACTIVE
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    companies = relationship('Company', back_populates="client", cascade='all, delete-orphan')
    emails = relationship('Email', back_populates="client")
