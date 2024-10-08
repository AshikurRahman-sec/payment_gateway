from sqlalchemy.orm import Session
from . import models, schemas
import uuid

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_payment_form(db: Session, form: schemas.PaymentFormCreate, user_id: int):
    db_form = models.PaymentForm(
        name=form.name,
        description=form.description,
        amount=form.amount,
        currency=form.currency,
        user_id=user_id
    )
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return db_form

def get_payment_forms_by_user(db: Session, user_id: int):
    return db.query(models.PaymentForm).filter(models.PaymentForm.user_id == user_id).all()

def get_payment_form_by_id(db: Session, form_id: int):
    return db.query(models.PaymentForm).filter(models.PaymentForm.id == form_id).first()

def create_transaction(db: Session, form_id: int, payment: schemas.PaymentCreate):
    db_transaction = models.Transaction(
        form_id=form_id,
        payer_email=payment.payer_email,
        amount_paid=payment.amount_paid,
        currency=payment.currency
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions_by_form_id(db: Session, form_id: int):
    return db.query(models.Transaction).filter(models.Transaction.form_id == form_id).all()

def create_payment_form(db: Session, form: schemas.PaymentFormCreate, user_id: int):
    db_form = models.PaymentForm(
        name=form.name,
        description=form.description,
        amount=form.amount,
        currency=form.currency,
        user_id=user_id,
        slug=str(uuid.uuid4())  # Generate unique slug on creation
    )
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return db_form
