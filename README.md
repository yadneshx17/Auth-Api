# FastAPI Authentication Template

A comprehensive authentication template for FastAPI applications with JWT tokens, refresh tokens, and secure user management.

## 🏗️ System Architecture

### Core Components
- **FastAPI Application**: Modern async web framework
- **SQLAlchemy 2.0**: Async ORM for database operations
- **JWT Authentication**: Access and refresh token system
- **Bcrypt Password Hashing**: Secure password storage
- **Pydantic Schemas**: Data validation and serialization

### Authentication Flow
```
1. User Signup → Hash Password → Store User
2. User Login → Validate Credentials → Generate JWT Tokens
3. Access Token (15 min) → API Requests
4. Refresh Token (7 days) → Token Renewal
5. Logout → Invalidate Refresh Token
```

## 📁 Folder Structure

```
AuthApi/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Environment configuration
│   ├── core/
│   │   ├── __init__.py
│   │   ├── dependencies.py     # Auth dependencies
│   │   └── security.py         # JWT & password utilities
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py         # Database session setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py            # User model
│   │   └── refresh_token.py   # Refresh token model
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py            # Pydantic schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   └── auth.py            # Auth endpoints
│   └── auth_service/
│       ├── __init__.py
│       └── auth_service.py    # Business logic
├── requirements.txt
└── .env                       # Environment variables
```

## 🔐 API Endpoints

### Authentication Endpoints

#### `POST /auth/signup`
Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com"
}
```

#### `POST /auth/login`
Authenticate user and generate tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### `GET /auth/me`
Get current user profile (requires authentication).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### `POST /auth/refresh`
Generate new access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### `POST /auth/logout`
Invalidate refresh token (requires authentication).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "message": "Logged out"
}
```

### Health Check

#### `GET /ping`
Simple health check endpoint.

**Response:**
```json
{
  "message": "pong"
}
```

## 🎫 Token Details

### Access Token
- **Purpose**: Authenticate API requests
- **Lifetime**: 15 minutes (configurable)
- **Algorithm**: HS256
- **Header**: `Authorization: Bearer <access_token>`

### Refresh Token
- **Purpose**: Generate new access tokens
- **Lifetime**: 7 days
- **Storage**: Database (invalidated on logout)
- **Usage**: Submit to `/auth/refresh` endpoint

### Token Payload
```json
{
  "sub": "user@example.com",
  "exp": 1640995200,
  "iat": 1640991600
}
```

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- Database (SQLite, PostgreSQL, etc.)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd AuthApi
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run the application:**
```bash
uvicorn app.main:app --reload
```

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
database_url=sqlite+aiosqlite:///./auth.db
alembic_database_url=sqlite:///./auth.db

# JWT Configuration
jwt_secret=your-super-secret-jwt-key-here
jwt_algorithm=HS256
access_token_expire_minutes=15
```

## 🛡️ Security Features

- **Password Hashing**: Bcrypt with salt
- **JWT Tokens**: Secure token-based authentication
- **Token Expiration**: Automatic token invalidation
- **Refresh Token Rotation**: Secure token renewal
- **CORS Protection**: Configurable origin restrictions
- **SQL Injection Prevention**: SQLAlchemy ORM protection

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### Refresh Tokens Table
```sql
CREATE TABLE refresh_tokens (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

## 🔧 Usage Examples

### Python Client
```python
import httpx

# Login
response = httpx.post("http://localhost:8000/auth/login", json={
    "email": "user@example.com",
    "password": "password123"
})
tokens = response.json()

# Access protected endpoint
headers = {"Authorization": f"Bearer {tokens['access_token']}"}
response = httpx.get("http://localhost:8000/auth/me", headers=headers)
user = response.json()
```

### JavaScript Client
```javascript
// Login
const loginResponse = await fetch('/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});
const { access_token, refresh_token } = await loginResponse.json();

// Access protected endpoint
const userResponse = await fetch('/auth/me', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
const user = await userResponse.json();
```

