# app/models.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    forms = relationship("PaymentForm", back_populates="owner")

class PaymentForm(Base):
    __tablename__ = "payment_forms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    amount = Column(Float)
    currency = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    slug = Column(String, unique=True, index=True, default=str(uuid.uuid4()))  # Unique slug

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    form_id = Column(Integer, ForeignKey("payment_forms.id"), nullable=False)
    payer_email = Column(String(100), nullable=False)
    amount_paid = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False)
    timestamp = Column(DateTime, default=func.now())

    payment_form = relationship("PaymentForm", back_populates="transactions")

