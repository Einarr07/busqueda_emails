from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, UniqueConstraint, Enum, func
from sqlalchemy.orm import relationship

from .common import IsActiveEnum
from ..db import Base


class Company(Base):
    __tablename__ = "companies"
    __table_args__ = (
        UniqueConstraint('client_id', 'name', name='uq_company_client_name'),
    )

    id_company = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    domain = Column(String(255), nullable=True)

    client_id = Column(Integer, ForeignKey("clients.id_client"), nullable=False, index=True)

    is_active = Column(
        Enum(IsActiveEnum, name="company_is_active_enum"),
        nullable=False,
        default=IsActiveEnum.ACTIVE,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    client = relationship('Client', back_populates="companies")
    emails = relationship('Email', back_populates='company')
