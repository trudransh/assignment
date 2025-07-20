
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from . import models, schemas
from .auth import get_password_hash

# User CRUD operations
def get_user_by_phone(db: Session, phone_number: str):
    """Get user by phone number"""
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Create a new user"""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        phone_number=user.phone_number,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Form submission CRUD operations
def get_form_submission(db: Session, submission_id: int):
    """Get form submission by ID"""
    return db.query(models.FormSubmission).filter(models.FormSubmission.id == submission_id).first()

def get_form_submissions(db: Session, skip: int = 0, limit: int = 10, user_id: Optional[int] = None):
    """Get form submissions with pagination and optional user filtering"""
    query = db.query(models.FormSubmission)
    if user_id:
        query = query.filter(models.FormSubmission.user_id == user_id)
    
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }

def create_form_submission(db: Session, form: schemas.FormCreate, user_id: Optional[int] = None):
    """Create a new form submission"""
    db_form = models.FormSubmission(
        name=form.name,
        phone_number=form.phone_number,
        email=form.email,
        address=form.address,
        user_id=user_id
    )
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return db_form

def update_form_submission(db: Session, submission_id: int, form_update: schemas.FormUpdate):
    """Update an existing form submission"""
    db_form = db.query(models.FormSubmission).filter(models.FormSubmission.id == submission_id).first()
    if db_form:
        update_data = form_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_form, field, value)
        db.commit()
        db.refresh(db_form)
    return db_form

def delete_form_submission(db: Session, submission_id: int):
    """Delete a form submission"""
    db_form = db.query(models.FormSubmission).filter(models.FormSubmission.id == submission_id).first()
    if db_form:
        db.delete(db_form)
        db.commit()
    return db_form

# KPA-Specific CRUD Operations

# Wheel Specification CRUD
def create_wheel_specification(db: Session, wheel_spec: schemas.WheelSpecificationCreate, user_id: Optional[int] = None):
    """Create a new wheel specification form"""
    db_wheel_spec = models.WheelSpecification(
        form_number=wheel_spec.formNumber,
        submitted_by=wheel_spec.submittedBy,
        submitted_date=wheel_spec.submittedDate,
        fields=wheel_spec.fields.dict(),
        user_id=user_id
    )
    db.add(db_wheel_spec)
    db.commit()
    db.refresh(db_wheel_spec)
    return db_wheel_spec

def get_wheel_specifications(
    db: Session, 
    form_number: Optional[str] = None,
    submitted_by: Optional[str] = None, 
    submitted_date: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
):
    """Get wheel specifications with optional filtering"""
    query = db.query(models.WheelSpecification)
    
    if form_number:
        query = query.filter(models.WheelSpecification.form_number == form_number)
    if submitted_by:
        query = query.filter(models.WheelSpecification.submitted_by == submitted_by)
    if submitted_date:
        query = query.filter(models.WheelSpecification.submitted_date == submitted_date)
    
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }

def get_wheel_specification_by_form_number(db: Session, form_number: str):
    """Get wheel specification by form number"""
    return db.query(models.WheelSpecification).filter(models.WheelSpecification.form_number == form_number).first()

# Bogie Checksheet CRUD
def create_bogie_checksheet(db: Session, bogie_checksheet: schemas.BogieChecksheetCreate, user_id: Optional[int] = None):
    """Create a new bogie checksheet form"""
    db_bogie_checksheet = models.BogieChecksheet(
        form_number=bogie_checksheet.formNumber,
        inspection_by=bogie_checksheet.inspectionBy,
        inspection_date=bogie_checksheet.inspectionDate,
        bogie_details=bogie_checksheet.bogieDetails.dict(),
        bogie_checksheet=bogie_checksheet.bogieChecksheet.dict(),
        bmbc_checksheet=bogie_checksheet.bmbcChecksheet.dict(),
        user_id=user_id
    )
    db.add(db_bogie_checksheet)
    db.commit()
    db.refresh(db_bogie_checksheet)
    return db_bogie_checksheet

def get_bogie_checksheets(
    db: Session,
    form_number: Optional[str] = None,
    inspection_by: Optional[str] = None,
    inspection_date: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
):
    """Get bogie checksheets with optional filtering"""
    query = db.query(models.BogieChecksheet)
    
    if form_number:
        query = query.filter(models.BogieChecksheet.form_number == form_number)
    if inspection_by:
        query = query.filter(models.BogieChecksheet.inspection_by == inspection_by)
    if inspection_date:
        query = query.filter(models.BogieChecksheet.inspection_date == inspection_date)
    
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }

def get_bogie_checksheet_by_form_number(db: Session, form_number: str):
    """Get bogie checksheet by form number"""
    return db.query(models.BogieChecksheet).filter(models.BogieChecksheet.form_number == form_number).first()
