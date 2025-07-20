# KPA Form Data API

A secure REST API for managing form submissions with JWT authentication, built with FastAPI and PostgreSQL.

## 🚀 Features

- **JWT Authentication** - Secure login with phone number and password
- **Form Data Management** - CRUD operations for form submissions
- **PostgreSQL Integration** - Robust database storage
- **API Documentation** - Auto-generated Swagger UI
- **Input Validation** - Pydantic schemas for data validation
- **Pagination Support** - Efficient data retrieval

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with bcrypt password hashing
- **Validation**: Pydantic schemas
- **Environment Management**: python-dotenv

## 📋 Implemented APIs

### 1. Authentication API
- **POST** `/v1/auth/login` - User login with phone number and password
- **POST** `/v1/auth/register` - New user registration

### 2. Form Data Manipulation API
- **POST** `/v1/form-data` - Create new form submission (authenticated)
- **GET** `/v1/form-data` - Get all form submissions with pagination (authenticated)
- **GET** `/v1/form-data/{id}` - Get specific form submission (authenticated)
- **PUT** `/v1/form-data/{id}` - Update form submission (authenticated)
- **DELETE** `/v1/form-data/{id}` - Delete form submission (authenticated)

## 🔧 Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL database (local or cloud)

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd postman-collection
pip install -r requirements.txt
```

### 2. Database Configuration
1. Get a free PostgreSQL database from [ElephantSQL](https://www.elephantsql.com/) or use local PostgreSQL
2. Update `.env` file with your database URL:
```env
DATABASE_URL=postgresql://username:password@hostname:port/database_name
SECRET_KEY=your-secret-key-here
```

### 3. Database Setup
```bash
python setup_database.py
```

### 4. Start the Server
```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

## 📖 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Authentication

### Default User Credentials (for testing)
- **Phone Number**: `7760873976`
- **Password**: `to_share@123`

### Usage Flow
1. **Login**: POST `/v1/auth/login` with phone number and password
2. **Get Token**: Copy the `access_token` from response
3. **Use Token**: Add `Authorization: Bearer <access_token>` header to protected endpoints

## 🧪 Testing with Postman

1. Import the `KPA_form_data.postman_collection.json` file
2. Set environment variables:
   - `base_url`: `http://localhost:8000`
   - `access_token`: (will be set after login)
3. Test the authentication flow:
   - Run the Login request
   - Copy the access_token to the environment variable
   - Test the form data endpoints

## 📁 Project Structure

```
postman-collection/
├── app/
│   ├── __init__.py
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   ├── crud.py           # Database operations
│   ├── auth.py           # Authentication utilities
│   └── database.py       # Database configuration
├── main.py               # FastAPI application
├── setup_database.py     # Database setup script
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── KPA_form_data.postman_collection.json
└── README.md
```

## 🔍 API Endpoints Details

### Authentication
```http
POST /v1/auth/login
Content-Type: application/json

{
    "phone_number": "7760873976",
    "password": "to_share@123"
}
```

### Form Data Operations
```http
# Create form data
POST /v1/form-data
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "John Doe",
    "phone_number": "9876543210",
    "email": "john@example.com",
    "address": "123 Main Street"
}
```

## 🚨 Environment Variables

Create a `.env` file with:
```env
DATABASE_URL=postgresql://username:password@hostname:port/database_name
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
```

## ⚠️ Limitations & Assumptions

1. **Database**: Requires PostgreSQL database setup
2. **Authentication**: Uses simple phone number + password (no OTP verification)
3. **Authorization**: Basic JWT implementation without role-based access
4. **File Uploads**: Not implemented in current version
5. **Rate Limiting**: Not implemented

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy ORM
- Environment-based configuration

## 📞 Support

For setup issues or questions, check:
1. Database connection in `.env` file
2. All dependencies installed: `pip install -r requirements.txt`
3. Database setup completed: `python setup_database.py`
4. API documentation: http://localhost:8000/docs

---

**Developed for KPA ERP Assignment**  
*FastAPI + PostgreSQL + JWT Authentication*