# app/api.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app import models, schemas, crud
from app.database import get_db
from .security import get_current_user, verify_password, create_access_token
from fastapi import BackgroundTasks
from fastapi import Request  
from typing import List
from datetime import timedelta
import os

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def hash_password(password: str):
    return pwd_context.hash(password)

@router.post("/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    new_user = crud.create_user(db=db, user=user, hashed_password=hashed_password)
    return new_user

@router.post("/forms/", response_model=schemas.PaymentForm)
def create_payment_form(
    form: schemas.PaymentFormCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_payment_form(db=db, form=form, user_id=current_user.id)

# Route to get all payment forms created by the current user
@router.get("/forms/", response_model=List[schemas.PaymentForm])
def get_payment_forms(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_payment_forms_by_user(db=db, user_id=current_user.id)

@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forms/{form_id}/payment", response_model=schemas.Transaction)
def make_payment(
    form_id: int,
    payment: schemas.PaymentCreate,
    db: Session = Depends(get_db)
):
    form = crud.get_payment_form_by_id(db=db, form_id=form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Payment form not found")

    # Log the payment transaction
    transaction = crud.create_transaction(db=db, form_id=form_id, payment=payment)

    # Notify the payment form owner
    form_owner = crud.get_user_by_id(db=db, user_id=form.user_id)
    send_payment_notification(form_owner.email, transaction)

    return transaction

def send_payment_notification(to_email: str, transaction: models.Transaction):
    print(f"Sending email to {to_email}: Payment of {transaction.amount_paid} {transaction.currency} made.")


@router.post("/forms/{form_id}/payment", response_model=schemas.Transaction)
def make_payment(
    form_id: int,
    payment: schemas.PaymentCreate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = Depends()
):
    form = crud.get_payment_form_by_id(db=db, form_id=form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Payment form not found")

    # Log the payment transaction
    transaction = crud.create_transaction(db=db, form_id=form_id, payment=payment)

    # Notify the payment form owner
    form_owner = crud.get_user_by_id(db=db, user_id=form.user_id)
    background_tasks.add_task(send_payment_notification, form_owner.email, transaction)

    return transaction

@router.post("/forms/", response_model=schemas.PaymentForm)
def create_payment_form(
    form: schemas.PaymentFormCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    request: Request = None  # Add request to access base URL
):
    payment_form = crud.create_payment_form(db=db, form=form, user_id=current_user.id)

    # Generate shareable link
    base_url = request.url_for('make_payment', form_id=payment_form.id)  # Get base URL for form payment
    shareable_url = f"{base_url}/{payment_form.slug}"

    return {
        "payment_form": payment_form,
        "shareable_url": shareable_url
    }

@router.post("/forms/payment/{slug}", response_model=schemas.Transaction)
def make_payment(
    slug: str,
    payment: schemas.PaymentCreate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = Depends()
):
    form = crud.get_payment_form_by_slug(db=db, slug=slug)
    if not form:
        raise HTTPException(status_code=404, detail="Payment form not found")

    # Log the payment transaction
    transaction = crud.create_transaction(db=db, form_id=form.id, payment=payment)

    # Notify the payment form owner
    form_owner = crud.get_user_by_id(db=db, user_id=form.user_id)
    background_tasks.add_task(send_payment_notification, form_owner.email, transaction)

    return transaction

def get_payment_form_by_slug(db: Session, slug: str):
    return db.query(models.PaymentForm).filter(models.PaymentForm.slug == slug).first()
