from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
import datetime

# Authentication Schemas
class UserLogin(BaseModel):
    phone_number: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    phone_number: Optional[str] = None

class UserBase(BaseModel):
    phone_number: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True

# Base schema for form data
class FormBase(BaseModel):
    name: str
    phone_number: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None

# Schema for creating a new form entry (used in POST request)
class FormCreate(FormBase):
    pass

# Schema for updating form entry (used in PUT request)
class FormUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None

# Schema for reading a form entry (used in API response)
class Form(FormBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

# Schema for pagination
class FormList(BaseModel):
    items: List[Form]
    total: int
    skip: int
    limit: int

# KPA-Specific Schemas matching Postman collection

# Wheel Specification Schemas
class WheelSpecificationFields(BaseModel):
    treadDiameterNew: Optional[str] = None
    lastShopIssueSize: Optional[str] = None
    condemningDia: Optional[str] = None
    wheelGauge: Optional[str] = None
    variationSameAxle: Optional[str] = None
    variationSameBogie: Optional[str] = None
    variationSameCoach: Optional[str] = None
    wheelProfile: Optional[str] = None
    intermediateWWP: Optional[str] = None
    bearingSeatDiameter: Optional[str] = None
    rollerBearingOuterDia: Optional[str] = None
    rollerBearingBoreDia: Optional[str] = None
    rollerBearingWidth: Optional[str] = None
    axleBoxHousingBoreDia: Optional[str] = None
    wheelDiscWidth: Optional[str] = None

class WheelSpecificationCreate(BaseModel):
    formNumber: str
    submittedBy: str
    submittedDate: str
    fields: WheelSpecificationFields

class WheelSpecificationResponse(BaseModel):
    formNumber: str
    submittedBy: str
    submittedDate: str
    status: str
    fields: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

# Bogie Checksheet Schemas
class BogieDetails(BaseModel):
    bogieNo: Optional[str] = None
    makerYearBuilt: Optional[str] = None
    incomingDivAndDate: Optional[str] = None
    deficitComponents: Optional[str] = None
    dateOfIOH: Optional[str] = None

class BogieChecksheetFields(BaseModel):
    bogieFrameCondition: Optional[str] = None
    bolster: Optional[str] = None
    bolsterSuspensionBracket: Optional[str] = None
    lowerSpringSeat: Optional[str] = None
    axleGuide: Optional[str] = None

class BmbcChecksheetFields(BaseModel):
    cylinderBody: Optional[str] = None
    pistonTrunnion: Optional[str] = None
    adjustingTube: Optional[str] = None
    plungerSpring: Optional[str] = None

class BogieChecksheetCreate(BaseModel):
    formNumber: str
    inspectionBy: str
    inspectionDate: str
    bogieDetails: BogieDetails
    bogieChecksheet: BogieChecksheetFields
    bmbcChecksheet: BmbcChecksheetFields

class BogieChecksheetResponse(BaseModel):
    formNumber: str
    inspectionBy: str
    inspectionDate: str
    status: str

    class Config:
        from_attributes = True

# Standard API Response Format matching Postman collection
class KPASuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Dict[str, Any]

class KPAListResponse(BaseModel):
    success: bool = True
    message: str
    data: List[Dict[str, Any]]