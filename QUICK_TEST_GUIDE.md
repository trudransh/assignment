# ⚡ Quick Test Guide (5 Minutes)

**For evaluators who want to test the API immediately without any setup**

## 🚀 Fastest Way to Test (3 Commands)

### Option A: Use Our Pre-hosted Demo
```bash
# Test our live demo API (no setup required)
curl -X POST https://your-demo-api.herokuapp.com/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "7760873976", "password": "to_share@123"}'
```

### Option B: Local Setup (5 minutes)
```bash
# 1. Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pydantic bcrypt python-jose passlib

# 2. Get free database
# Visit: https://www.elephantsql.com/ → Sign up → Create database → Copy URL

# 3. Set environment (replace DATABASE_URL)
export DATABASE_URL="postgresql://your-url-here"
export SECRET_KEY="test-secret-key"

# 4. Initialize and start
python3 setup_database.py
uvicorn main:app --reload
```

## 🧪 Test Commands (Copy-Paste Ready)

**Test 1: Authentication**
```bash
curl -X POST http://localhost:8000/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "7760873976", "password": "to_share@123"}'
```

**Test 2: Submit Form**
```bash
curl -X POST http://localhost:8000/api/forms/wheel-specifications \
  -H "Content-Type: application/json" \
  -d '{
    "formNumber": "EVAL-TEST-001",
    "submittedBy": "evaluator",
    "submittedDate": "2025-01-21",
    "fields": {"treadDiameterNew": "915", "wheelGauge": "1600"}
  }'
```

**Test 3: Retrieve Data**
```bash
curl http://localhost:8000/api/forms/wheel-specifications
```

## ✅ Expected Results

1. **Login**: Returns JWT token
2. **Submit**: Returns `{"success": true, "message": "submitted successfully"}`
3. **Retrieve**: Returns list with submitted data

## 🌐 Browser Test

Visit: `http://localhost:8000/docs`
- Interactive API documentation
- Test all endpoints directly
- No command line needed

## 🚨 If Something Fails

**Database Issues**: Use SQLite instead
```bash
# Quick SQLite setup (no external database needed)
export DATABASE_URL="sqlite:///./test.db"
python3 setup_database.py
uvicorn main:app --reload
```

**Port Issues**: Use different port
```bash
uvicorn main:app --port 8001
# Then test with: http://localhost:8001
```

---

**🎯 Total time: 3-5 minutes to verify all APIs are working** 