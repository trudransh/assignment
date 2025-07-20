
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    # Relationship to form submissions
    form_submissions = relationship("FormSubmission", back_populates="user")
    wheel_specifications = relationship("WheelSpecification", back_populates="user")
    bogie_checksheets = relationship("BogieChecksheet", back_populates="user")

class FormSubmission(Base):
    __tablename__ = "form_submissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Foreign key to user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="form_submissions")

# KPA Specific Models matching the Postman collection

class WheelSpecification(Base):
    __tablename__ = "wheel_specifications"

    id = Column(Integer, primary_key=True, index=True)
    form_number = Column(String(100), unique=True, nullable=False, index=True)
    submitted_by = Column(String(100), nullable=False)
    submitted_date = Column(String(20), nullable=False)  # Store as string to match API
    status = Column(String(50), default="Saved")
    
    # Store the complex fields as JSON to match the API structure
    fields = Column(JSON, nullable=False)
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Foreign key to user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="wheel_specifications")

class BogieChecksheet(Base):
    __tablename__ = "bogie_checksheets"

    id = Column(Integer, primary_key=True, index=True)
    form_number = Column(String(100), unique=True, nullable=False, index=True)
    inspection_by = Column(String(100), nullable=False)
    inspection_date = Column(String(20), nullable=False)  # Store as string to match API
    status = Column(String(50), default="Saved")
    
    # Store the complex nested data as JSON
    bogie_details = Column(JSON, nullable=False)
    bogie_checksheet = Column(JSON, nullable=False)
    bmbc_checksheet = Column(JSON, nullable=False)
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Foreign key to user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="bogie_checksheets")
