# 🚀 KPA Flutter App Setup Guide

Your Flutter frontend is now **fully integrated** with the KPA Form Data API! Here's how to set it up and run it.

## 📋 What's Been Implemented

### ✅ **Complete Integration**
- **KPA Authentication Service** - JWT login with your backend
- **KPA Form Service** - Direct API calls to your FastAPI backend
- **Updated Login Screen** - Now connects to your local API
- **ICF Wheel Form** - Submits data to `/api/forms/wheel-specifications`
- **Real-time API Integration** - Live connection to `http://localhost:8000`

### ✅ **New Features Added**
1. **KPA Login Form** (`lib/user_screen/form/kpa_login_form.dart`)
   - Pre-filled with test credentials: `7760873976` / `to_share@123`
   - Direct connection to your JWT API
   - Token management with SharedPreferences

2. **KPA Authentication Service** (`lib/services/authentication_services/kpa_auth_service.dart`)
   - Login, register, token storage
   - Automatic authentication headers

3. **KPA Form Service** (`lib/services/api_services/kpa_form_service.dart`)
   - Wheel specification submission
   - Bogie checksheet submission
   - Form data retrieval with filtering

4. **Enhanced ICF Wheel Provider** (`lib/provider/icf_wheel_provider.dart`)
   - Real API submission to your backend
   - Form validation and error handling
   - Success/failure feedback

## 🛠️ Setup Instructions

### 1. Install Flutter (if not already installed)
```bash
# Install Flutter SDK
sudo snap install flutter --classic

# Or download from: https://flutter.dev/docs/get-started/install
```

### 2. Setup the Flutter App
```bash
# Navigate to Flutter project
cd flutter_frontend

# Get dependencies
flutter pub get

# Check Flutter setup
flutter doctor -v
```

### 3. Start Your Backend API
```bash
# Make sure your FastAPI backend is running
cd ../  # Back to main project
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Run the Flutter App
```bash
# In flutter_frontend directory
flutter run

# Or for web
flutter run -d chrome

# Or for specific device
flutter devices  # List available devices
flutter run -d <device-id>
```

## 📱 **How to Use the Integrated App**

### **Step 1: Login**
1. App opens to the **KPA Login Screen**
2. Default credentials are pre-filled:
   - **Phone**: `7760873976`
   - **Password**: `to_share@123`
3. Click **"Login to KPA API"**
4. Success → Navigate to Home Screen

### **Step 2: Submit Wheel Specification**
1. From Home → Navigate to **"ICF Wheel"** form
2. Form fields are pre-populated with test data
3. **Form Number** is auto-generated (e.g., `WHEEL-2025-123456`)
4. **Submitted By** defaults to `flutter_user`
5. Click **"Submit to KPA API"**
6. Success → See green confirmation with form number

### **Step 3: Verify in Backend**
```bash
# Check your PostgreSQL database
# Or call the GET API:
curl http://localhost:8000/api/forms/wheel-specifications
```

## 🔧 **API Endpoints Used**

| Flutter Function | API Endpoint | Method |
|------------------|--------------|---------|
| Login | `/v1/auth/login` | POST |
| Submit Wheel Spec | `/api/forms/wheel-specifications` | POST |
| Get Wheel Specs | `/api/forms/wheel-specifications` | GET |
| Submit Bogie | `/api/forms/bogie-checksheet` | POST |
| Get Bogie | `/api/forms/bogie-checksheet` | GET |

## 🏗️ **File Structure Changes**

```
flutter_frontend/
├── lib/
│   ├── constants/
│   │   └── api_constant.dart          # ✅ Updated to localhost:8000
│   ├── services/
│   │   ├── api_services/
│   │   │   └── kpa_form_service.dart  # 🆕 KPA form APIs
│   │   └── authentication_services/
│   │       └── kpa_auth_service.dart  # 🆕 KPA auth service
│   ├── user_screen/form/
│   │   └── kpa_login_form.dart        # 🆕 KPA login form
│   ├── screens/Home_screen/
│   │   └── icf_wheel.dart             # ✅ Updated with API integration
│   └── provider/
│       └── icf_wheel_provider.dart    # ✅ Updated with real API calls
```

## 🎯 **Testing the Integration**

### **Test 1: Authentication**
```bash
# Should work with Flutter login
curl -X POST http://localhost:8000/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "7760873976", "password": "to_share@123"}'
```

### **Test 2: Form Submission**
1. Login to Flutter app
2. Fill out wheel specification form
3. Submit → Should see success message
4. Verify in database or via:
```bash
curl http://localhost:8000/api/forms/wheel-specifications
```

## 🚨 **Troubleshooting**

### **Flutter Not Found**
```bash
# Install Flutter
sudo snap install flutter --classic
# Or follow: https://flutter.dev/docs/get-started/install
```

### **API Connection Issues**
1. **Check Backend**: Ensure FastAPI is running on `localhost:8000`
2. **Check CORS**: Already configured in your `main.py`
3. **Check Network**: Flutter and API on same machine

### **Android Network Issues**
If running on Android emulator, update API URL:
```dart
// In flutter_frontend/lib/constants/api_constant.dart
static const String baseUrl = 'http://10.0.2.2:8000';  // For Android emulator
```

### **Common Errors**
- **"Connection refused"** → Backend not running
- **"Login failed"** → Check credentials or API endpoint
- **"Build failed"** → Run `flutter clean && flutter pub get`

## 🎉 **Success Criteria**

✅ **Login works** → JWT token received and stored  
✅ **Form submission works** → Data appears in PostgreSQL  
✅ **Real-time connection** → No mock data, actual API calls  
✅ **Error handling** → Proper error messages for failures  
✅ **User feedback** → Loading states, success messages  

## 📊 **Demo Flow for Video**

1. **Start Backend**: `uvicorn main:app --reload`
2. **Start Flutter**: `flutter run`
3. **Login**: Use pre-filled credentials
4. **Navigate**: Go to ICF Wheel form
5. **Submit**: Fill and submit form
6. **Verify**: Show success message
7. **Check API**: `curl` to verify data

## 🔗 **Next Steps**

1. **Add Bogie Checksheet Form** → Similar integration pattern
2. **Add Form Listing** → Show submitted forms from API
3. **Add Authentication** → Implement logout, token refresh
4. **Add Validation** → Enhanced form validation
5. **Add Offline Support** → Local storage for offline forms

---

## 🎯 **Assignment Completion Status**

### ✅ **Frontend Integration: COMPLETE**
- Flutter app connects to your FastAPI backend
- Real form submission and authentication
- Live API integration without mock data
- Production-ready Flutter codebase

### 🏆 **Ready for Demonstration**
Your Flutter app is now fully integrated and ready for the assignment demo video! 