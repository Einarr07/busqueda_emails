from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, UniqueConstraint, Text, func
from sqlalchemy.orm import relationship

from ..db import Base


class Email(Base):
    __tablename__ = 'emails'
    __table_args__ = (
        UniqueConstraint("smtp_provider", "smtp_message_id", name="uq_email_smtp_provider_msgid"),
    )

    id_email = Column(Integer, primary_key=True, index=True, autoincrement=True)

    client_id = Column(Integer, ForeignKey('clients.id_client'), nullable=False, index=True)
    company_id = Column(Integer, ForeignKey('companies.id_company'), nullable=False, index=True)

    sender = Column(String(255), nullable=False)
    recipient = Column(String(255), nullable=False)
    sent_at = Column(DateTime(timezone=True), nullable=False)

    smtp_provider = Column(String(50), nullable=False)
    smtp_message_id = Column(String(255), nullable=False)

    subject = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    client = relationship('Client', back_populates='emails')
    company = relationship('Company', back_populates='emails')
