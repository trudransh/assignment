# Flutter Frontend Integration Guide

This guide explains how to integrate the KPA Form Data API with a Flutter frontend application.

## 🚀 Quick Start

### 1. API Configuration

Your FastAPI backend is already configured with CORS middleware to allow Flutter connections.

**Base URL**: `http://localhost:8000` (development)
**Production URL**: Replace with your deployed API URL

### 2. Flutter Dependencies

Add these dependencies to your `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0
  dio: ^5.3.2  # Alternative to http
  shared_preferences: ^2.2.2  # For token storage
  provider: ^6.1.1  # State management
```

### 3. API Service Implementation

Create `lib/services/api_service.dart`:

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000';
  
  // Get stored token
  Future<String?> getToken() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.getString('access_token');
  }
  
  // Save token
  Future<void> saveToken(String token) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setString('access_token', token);
  }
  
  // Login
  Future<Map<String, dynamic>> login(String phoneNumber, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/v1/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'phone_number': phoneNumber,
        'password': password,
      }),
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      await saveToken(data['access_token']);
      return data;
    } else {
      throw Exception('Login failed: ${response.body}');
    }
  }
  
  // Submit Wheel Specification
  Future<Map<String, dynamic>> submitWheelSpecification(
    Map<String, dynamic> wheelSpec
  ) async {
    final token = await getToken();
    
    final response = await http.post(
      Uri.parse('$baseUrl/api/forms/wheel-specifications'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode(wheelSpec),
    );
    
    if (response.statusCode == 201) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Submit failed: ${response.body}');
    }
  }
  
  // Get Wheel Specifications
  Future<List<dynamic>> getWheelSpecifications() async {
    final token = await getToken();
    
    final response = await http.get(
      Uri.parse('$baseUrl/api/forms/wheel-specifications'),
      headers: {
        'Authorization': 'Bearer $token',
      },
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['data'];
    } else {
      throw Exception('Fetch failed: ${response.body}');
    }
  }
}
```

### 4. Login Screen Example

Create `lib/screens/login_screen.dart`:

```dart
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _phoneController = TextEditingController();
  final _passwordController = TextEditingController();
  final ApiService _apiService = ApiService();
  bool _isLoading = false;

  Future<void> _login() async {
    setState(() => _isLoading = true);
    
    try {
      await _apiService.login(
        _phoneController.text,
        _passwordController.text,
      );
      
      // Navigate to main screen
      Navigator.pushReplacementNamed(context, '/home');
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Login failed: $e')),
      );
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('KPA Login')),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _phoneController,
              decoration: InputDecoration(
                labelText: 'Phone Number',
                hintText: '7760873976',
              ),
            ),
            SizedBox(height: 16),
            TextField(
              controller: _passwordController,
              decoration: InputDecoration(labelText: 'Password'),
              obscureText: true,
            ),
            SizedBox(height: 32),
            _isLoading
                ? CircularProgressIndicator()
                : ElevatedButton(
                    onPressed: _login,
                    child: Text('Login'),
                  ),
          ],
        ),
      ),
    );
  }
}
```

### 5. Form Submission Example

Create `lib/screens/wheel_spec_form.dart`:

```dart
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class WheelSpecForm extends StatefulWidget {
  @override
  _WheelSpecFormState createState() => _WheelSpecFormState();
}

class _WheelSpecFormState extends State<WheelSpecForm> {
  final _formKey = GlobalKey<FormState>();
  final _formNumberController = TextEditingController();
  final _submittedByController = TextEditingController();
  final _treadDiameterController = TextEditingController();
  final _wheelGaugeController = TextEditingController();
  final ApiService _apiService = ApiService();

  Future<void> _submitForm() async {
    if (_formKey.currentState!.validate()) {
      try {
        final wheelSpec = {
          'formNumber': _formNumberController.text,
          'submittedBy': _submittedByController.text,
          'submittedDate': DateTime.now().toIso8601String().split('T')[0],
          'fields': {
            'treadDiameterNew': _treadDiameterController.text,
            'wheelGauge': _wheelGaugeController.text,
          }
        };

        final result = await _apiService.submitWheelSpecification(wheelSpec);
        
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Form submitted successfully!')),
        );
        
        // Clear form
        _formKey.currentState!.reset();
        
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Submission failed: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Wheel Specification Form')),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _formNumberController,
                decoration: InputDecoration(labelText: 'Form Number'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter form number';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _submittedByController,
                decoration: InputDecoration(labelText: 'Submitted By'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter submitted by';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _treadDiameterController,
                decoration: InputDecoration(labelText: 'Tread Diameter'),
              ),
              TextFormField(
                controller: _wheelGaugeController,
                decoration: InputDecoration(labelText: 'Wheel Gauge'),
              ),
              SizedBox(height: 32),
              ElevatedButton(
                onPressed: _submitForm,
                child: Text('Submit Form'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

## 🔧 Configuration for Production

### 1. Update Base URL

In production, update the `baseUrl` in `ApiService`:

```dart
static const String baseUrl = 'https://your-api-domain.com';
```

### 2. Network Security

Add to `android/app/src/main/AndroidManifest.xml`:

```xml
<application android:usesCleartextTraffic="true">
```

### 3. iOS Configuration

Add to `ios/Runner/Info.plist`:

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

## 📱 Testing the Integration

1. Start your FastAPI backend: `uvicorn main:app --reload`
2. Run your Flutter app: `flutter run`
3. Test login with: Phone: `7760873976`, Password: `to_share@123`
4. Submit forms and verify data appears in your PostgreSQL database

## 🚨 Error Handling

The API returns standardized error responses. Handle them in Flutter:

```dart
try {
  final result = await apiService.someMethod();
} on Exception catch (e) {
  if (e.toString().contains('401')) {
    // Token expired, redirect to login
    Navigator.pushReplacementNamed(context, '/login');
  } else {
    // Show error message
    showDialog(/* error dialog */);
  }
}
```

## 📋 Available API Endpoints

### Authentication
- `POST /v1/auth/login` - User login
- `POST /v1/auth/register` - User registration

### KPA Forms
- `POST /api/forms/wheel-specifications` - Submit wheel spec
- `GET /api/forms/wheel-specifications` - Get wheel specs
- `POST /api/forms/bogie-checksheet` - Submit bogie checksheet
- `GET /api/forms/bogie-checksheet` - Get bogie checksheets

### General Form Data
- `GET /v1/form-data` - Get all forms (with auth)
- `POST /v1/form-data` - Create form (with auth)
- `PUT /v1/form-data/{id}` - Update form (with auth)
- `DELETE /v1/form-data/{id}` - Delete form (with auth)

For detailed API documentation, visit: `http://localhost:8000/docs` 