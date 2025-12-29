# Civic-AI Authentication System

Complete authentication implementation using Supabase Auth with FastAPI.

## 🚀 Features

- **User Registration** - Sign up with name, email, and password
- **User Login** - Authenticate with email and password  
- **JWT Token Management** - Secure token-based authentication
- **Protected Routes** - Middleware for route protection
- **User Profile Management** - Store and retrieve user data
- **Error Handling** - Comprehensive error responses

## 📋 Prerequisites

1. **Supabase Project** - Create a project at [supabase.com](https://supabase.com)
2. **Python 3.8+** - Ensure Python is installed
3. **Environment Variables** - Configure Supabase credentials

## ⚙️ Setup Instructions

### 1. Install Dependencies

```bash
cd server
pip install -r requirements.txt
```

Or run the setup script:
```bash
python install_auth.py
```

### 2. Configure Environment Variables

Update `server/.env` with your Supabase credentials:

```env
CORS_ORIGIN=http://localhost:3000
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 3. Create Database Table

Execute this SQL in your Supabase SQL Editor:

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create policy for users to only access their own data
CREATE POLICY "Users can only access their own data" ON users
    FOR ALL USING (auth.uid() = id);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### 4. Start the Server

```bash
uvicorn main:app --reload
```

### 5. Test the Authentication

```bash
python test_auth.py
```

## 🔗 API Endpoints

### Public Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health status

### Authentication Endpoints

- `POST /auth/signup` - Create new user account
- `POST /auth/login` - Authenticate user
- `GET /auth/me` - Get current user (protected)

### Protected Endpoints

- `POST /api/query` - AI query processing (requires authentication)

## 📝 API Usage Examples

### Sign Up

```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com", 
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid-here",
    "email": "john@example.com",
    "name": "John Doe"
  },
  "message": "Account created successfully"
}
```

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid-here", 
    "email": "john@example.com",
    "name": "John Doe"
  },
  "message": "Login successful"
}
```

### Get Current User

```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response:**
```json
{
  "id": "uuid-here",
  "email": "john@example.com", 
  "name": "John Doe",
  "created_at": "2024-12-29T12:00:00Z"
}
```

### Protected Query

```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is PM-KISAN scheme?",
    "language": "en"
  }'
```

## 🔒 Security Features

- **JWT Token Validation** - All protected routes validate tokens
- **Row Level Security** - Database policies restrict data access
- **Password Hashing** - Supabase handles secure password storage
- **CORS Protection** - Configured for frontend origin only
- **Input Validation** - Pydantic models validate all requests

## 🚨 Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400` - Bad Request (validation errors, email already exists)
- `401` - Unauthorized (invalid credentials, expired token)
- `404` - Not Found (user profile not found)
- `500` - Internal Server Error (database/server issues)

## 🔧 Frontend Integration

The authentication system is ready to integrate with the existing frontend:

1. **Login/Signup Pages** - Already exist at `/login` and `/signup`
2. **Token Storage** - Frontend should store the `access_token`
3. **API Calls** - Include `Authorization: Bearer <token>` header
4. **Dashboard Protection** - Check token validity before accessing dashboard

## 📁 File Structure

```
server/
├── main.py              # Main FastAPI application with auth
├── requirements.txt     # Updated with Supabase dependencies  
├── .env                # Environment variables
├── install_auth.py     # Setup script
├── test_auth.py        # Authentication test suite
└── AUTH_README.md      # This documentation
```

## 🎯 Production Considerations

- **Environment Variables** - Use secure secret management
- **HTTPS** - Enable SSL/TLS in production
- **Rate Limiting** - Add rate limiting for auth endpoints
- **Logging** - Enhanced logging for security events
- **Token Refresh** - Implement refresh token rotation
- **Email Verification** - Enable email confirmation in Supabase

## 🐛 Troubleshooting

### Common Issues

1. **"SUPABASE_URL and SUPABASE_ANON_KEY must be set"**
   - Update your `.env` file with correct Supabase credentials

2. **"Failed to create user profile"**
   - Ensure the `users` table exists in your Supabase database

3. **"Invalid authentication credentials"**
   - Check that the token is valid and not expired

4. **CORS errors**
   - Verify the frontend URL matches the CORS configuration

### Getting Help

- Check the Supabase dashboard for auth logs
- Review the FastAPI automatic docs at `http://localhost:8000/docs`
- Run the test script to verify functionality: `python test_auth.py`

---

✅ **Authentication system is production-ready and demo-ready!**