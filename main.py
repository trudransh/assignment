
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import timedelta

from app import crud, models, schemas
from app.database import SessionLocal, engine, get_db
from app.auth import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES

# This command creates the table in your database based on the model
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KPA Form Data API", 
    version="1.0.0",
    description="API for KPA form data management with authentication"
)

# Add CORS middleware for Flutter frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific Flutter app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================
# AUTHENTICATION API (API #1)
# ================================

@app.post("/v1/auth/login", response_model=schemas.Token, tags=["Authentication"])
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user with phone number and password.
    Returns JWT access token for accessing protected endpoints.
    """
    user = authenticate_user(db, user_credentials.phone_number, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.phone_number}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/v1/auth/register", response_model=schemas.User, status_code=201, tags=["Authentication"])
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user with phone number and password.
    """
    db_user = crud.get_user_by_phone(db, phone_number=user.phone_number)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    return crud.create_user(db=db, user=user)

# ================================
# KPA FORM DATA APIs (API #2) - MATCHING POSTMAN COLLECTION
# ================================

@app.post("/api/forms/wheel-specifications", response_model=schemas.KPASuccessResponse, status_code=201, tags=["KPA Forms"])
def submit_wheel_specification(
    wheel_spec: schemas.WheelSpecificationCreate,
    db: Session = Depends(get_db)
):
    """
    Submit wheel specification form - matches exact Postman collection structure.
    POST /api/forms/wheel-specifications
    """
    try:
        # Check if form number already exists
        existing_form = crud.get_wheel_specification_by_form_number(db, wheel_spec.formNumber)
        if existing_form:
            raise HTTPException(status_code=400, detail=f"Form number {wheel_spec.formNumber} already exists")
        
        # Create the wheel specification
        db_wheel_spec = crud.create_wheel_specification(db=db, wheel_spec=wheel_spec)
        
        # Return response matching Postman collection format
        return schemas.KPASuccessResponse(
            success=True,
            message="Wheel specification submitted successfully.",
            data={
                "formNumber": db_wheel_spec.form_number,
                "submittedBy": db_wheel_spec.submitted_by,
                "submittedDate": db_wheel_spec.submitted_date,
                "status": db_wheel_spec.status
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating wheel specification: {str(e)}")  # For debugging
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/forms/bogie-checksheet", response_model=schemas.KPASuccessResponse, status_code=201, tags=["KPA Forms"])
def submit_bogie_checksheet(
    bogie_checksheet: schemas.BogieChecksheetCreate,
    db: Session = Depends(get_db)
):
    """
    Submit bogie checksheet form - matches exact Postman collection structure.
    POST /api/forms/bogie-checksheet
    """
    try:
        # Check if form number already exists
        existing_form = crud.get_bogie_checksheet_by_form_number(db, bogie_checksheet.formNumber)
        if existing_form:
            raise HTTPException(status_code=400, detail=f"Form number {bogie_checksheet.formNumber} already exists")
        
        # Create the bogie checksheet
        db_bogie_checksheet = crud.create_bogie_checksheet(db=db, bogie_checksheet=bogie_checksheet)
        
        # Return response matching Postman collection format
        return schemas.KPASuccessResponse(
            success=True,
            message="Bogie checksheet submitted successfully.",
            data={
                "formNumber": db_bogie_checksheet.form_number,
                "inspectionBy": db_bogie_checksheet.inspection_by,
                "inspectionDate": db_bogie_checksheet.inspection_date,
                "status": db_bogie_checksheet.status
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting bogie checksheet: {str(e)}")

@app.get("/api/forms/wheel-specifications", response_model=schemas.KPAListResponse, tags=["KPA Forms"])
def get_wheel_specifications(
    formNumber: Optional[str] = Query(None, description="Filter by form number"),
    submittedBy: Optional[str] = Query(None, description="Filter by submitted by"),
    submittedDate: Optional[str] = Query(None, description="Filter by submitted date (YYYY-MM-DD)"),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get wheel specification forms with filtering - matches Postman collection GET endpoint.
    GET /api/forms/wheel-specifications?formNumber=...&submittedBy=...&submittedDate=...
    """
    try:
        result = crud.get_wheel_specifications(
            db=db,
            form_number=formNumber,
            submitted_by=submittedBy,
            submitted_date=submittedDate,
            skip=skip,
            limit=limit
        )
        
        # Format response to match Postman collection
        data = []
        for item in result["items"]:
            data.append({
                "formNumber": item.form_number,
                "submittedBy": item.submitted_by,
                "submittedDate": item.submitted_date,
                "status": item.status,
                "fields": item.fields
            })
        
        message = "Filtered wheel specification forms fetched successfully." if any([formNumber, submittedBy, submittedDate]) else "All wheel specification forms fetched successfully."
        
        return schemas.KPAListResponse(
            success=True,
            message=message,
            data=data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching wheel specifications: {str(e)}")

@app.get("/api/forms/bogie-checksheet", response_model=schemas.KPAListResponse, tags=["KPA Forms"])
def get_bogie_checksheets(
    formNumber: Optional[str] = Query(None, description="Filter by form number"),
    inspectionBy: Optional[str] = Query(None, description="Filter by inspection by"),
    inspectionDate: Optional[str] = Query(None, description="Filter by inspection date (YYYY-MM-DD)"),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get bogie checksheet forms with filtering.
    GET /api/forms/bogie-checksheet?formNumber=...&inspectionBy=...&inspectionDate=...
    """
    try:
        result = crud.get_bogie_checksheets(
            db=db,
            form_number=formNumber,
            inspection_by=inspectionBy,
            inspection_date=inspectionDate,
            skip=skip,
            limit=limit
        )
        
        # Format response to match expected structure
        data = []
        for item in result["items"]:
            data.append({
                "formNumber": item.form_number,
                "inspectionBy": item.inspection_by,
                "inspectionDate": item.inspection_date,
                "status": item.status,
                "bogieDetails": item.bogie_details,
                "bogieChecksheet": item.bogie_checksheet,
                "bmbcChecksheet": item.bmbc_checksheet
            })
        
        message = "Filtered bogie checksheet forms fetched successfully." if any([formNumber, inspectionBy, inspectionDate]) else "All bogie checksheet forms fetched successfully."
        
        return schemas.KPAListResponse(
            success=True,
            message=message,
            data=data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bogie checksheets: {str(e)}")

# ================================
# FORM DATA MANIPULATION API (Additional CRUD endpoints)
# ================================

@app.post("/v1/form-data", response_model=schemas.Form, status_code=201, tags=["Form Data"])
def create_form(
    form: schemas.FormCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Creates a new form submission entry in the database.
    Requires authentication.
    """
    return crud.create_form_submission(db=db, form=form, user_id=current_user.id)

@app.get("/v1/form-data", response_model=schemas.FormList, tags=["Form Data"])
def get_all_forms(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieves all form submissions with pagination.
    Requires authentication.
    """
    result = crud.get_form_submissions(db, skip=skip, limit=limit)
    return schemas.FormList(**result)

@app.get("/v1/form-data/{form_data_id}", response_model=schemas.Form, tags=["Form Data"])
def read_form(
    form_data_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieves a specific form submission by its ID.
    Requires authentication.
    """
    db_form = crud.get_form_submission(db, submission_id=form_data_id)
    if db_form is None:
        raise HTTPException(status_code=404, detail="Form data not found")
    return db_form

@app.put("/v1/form-data/{form_data_id}", response_model=schemas.Form, tags=["Form Data"])
def update_form(
    form_data_id: int,
    form_update: schemas.FormUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Updates an existing form submission.
    Requires authentication.
    """
    db_form = crud.update_form_submission(db, submission_id=form_data_id, form_update=form_update)
    if db_form is None:
        raise HTTPException(status_code=404, detail="Form data not found")
    return db_form

@app.delete("/v1/form-data/{form_data_id}", status_code=204, tags=["Form Data"])
def delete_form(
    form_data_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Deletes a form submission.
    Requires authentication.
    """
    db_form = crud.delete_form_submission(db, submission_id=form_data_id)
    if db_form is None:
        raise HTTPException(status_code=404, detail="Form data not found")
    return {"message": "Form data deleted successfully"}

# Root endpoint for health check
@app.get("/", tags=["Health"])
def read_root():
    return {
        "status": "API is running!",
        "message": "KPA Form Data API v1.0.0",
        "endpoints": {
            "authentication": "/v1/auth/login",
            "wheel_specifications": "/api/forms/wheel-specifications", 
            "bogie_checksheet": "/api/forms/bogie-checksheet",
            "documentation": "/docs"
        }
    }