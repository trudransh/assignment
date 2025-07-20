#!/usr/bin/env python3
"""
Database setup script for KPA Form Data API
This script creates the database tables and adds a default user for testing.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User
from app.auth import get_password_hash
from dotenv import load_dotenv

def setup_database():
    """Setup database with tables and default user"""
    
    # Load environment variables
    load_dotenv()
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL or DATABASE_URL == "postgresql://username:password@localhost:5432/kpa_database":
        print("❌ Please update DATABASE_URL in .env file with your actual database credentials")
        print("Visit https://www.elephantsql.com/ for a free PostgreSQL database")
        return False
    
    try:
        # Create engine and session
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Create all tables
        print("🔄 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Create default user with credentials from assignment
        db = SessionLocal()
        try:
            # Check if user already exists
            existing_user = db.query(User).filter(User.phone_number == "7760873976").first()
            if not existing_user:
                default_user = User(
                    phone_number="7760873976",
                    hashed_password=get_password_hash("to_share@123"),
                    is_active=True
                )
                db.add(default_user)
                db.commit()
                print("✅ Default user created successfully!")
                print("   Phone: 7760873976")
                print("   Password: to_share@123")
            else:
                print("ℹ️  Default user already exists")
                
        except Exception as e:
            print(f"❌ Error creating default user: {e}")
            db.rollback()
        finally:
            db.close()
            
        print("\n🎉 Database setup completed!")
        print("🚀 You can now start the API server with: uvicorn main:app --reload")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please check your DATABASE_URL in .env file")
        return False

if __name__ == "__main__":
    setup_database() 