from pydantic import BaseModel
from typing import List, Optional
import datetime

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class PaymentFormBase(BaseModel):
    name: str
    description: Optional[str] = None
    amount: float
    currency: str

class PaymentCreate(BaseModel):
    payer_email: str
    amount_paid: float
    currency: str

class Transaction(BaseModel):
    id: int
    form_id: int
    payer_email: str
    amount_paid: float
    currency: str
    timestamp: datetime

    class Config:
        orm_mode = True

class PaymentForm(BaseModel):
    id: int
    name: str
    description: str
    amount: float
    currency: str
    slug: str  

    class Config:
        orm_mode = True
