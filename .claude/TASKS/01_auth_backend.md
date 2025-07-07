# System 01 — User & Auth Backend

**Status:** 🔴 not started  
**Narrative Avatar:** An Author  
**Service Port:** 8080  
**Container Name:** `auth-backend`

## Overview
FastAPI-based authentication service that integrates with Supabase for user management and JWT token verification. This is the foundational identity layer that all other services will depend on.

## Acceptance Criteria

### ✅ Core Routes
- [ ] `POST /signup` - Register new users via Supabase Admin API
- [ ] `POST /login` - Authenticate users and return JWT tokens
- [ ] `GET /me` - Get current user profile from JWT
- [ ] `GET /health` - Health check endpoint returning `{"status": "ok"}`

### ✅ Docker Integration
- [ ] Service runs in Docker container at `http://auth-backend:8080`
- [ ] Added to main `docker-compose.yml` with proper networking
- [ ] Uses `python:3.11-slim` base image
- [ ] Includes all necessary dependencies

### ✅ Environment Configuration
- [ ] `SUPABASE_URL` - Base URL for Supabase project
- [ ] `SUPABASE_JWT_SECRET` - Secret for JWT verification
- [ ] `SUPABASE_SERVICE_KEY` - Admin API key for user operations
- [ ] Updated `.env.example` with all required variables

### ✅ Testing
- [ ] `tests/test_auth_health.py` - Health check test
- [ ] `tests/test_auth_endpoints.py` - Authentication flow tests
- [ ] All tests pass with `pytest -q`

### ✅ Development Workflow
- [ ] `make dev` starts the service successfully
- [ ] Service logs show successful startup
- [ ] Health endpoint accessible at `http://localhost:8080/health`

## Technical Implementation

### Dependencies
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `supabase` - Python client for Supabase
- `python-jose[cryptography]` - JWT handling
- `passlib[bcrypt]` - Password hashing
- `python-multipart` - Form data handling

### Authentication Flow
1. **Signup**: Validate input → Create user in Supabase → Return success/error
2. **Login**: Validate credentials → Get JWT from Supabase → Return token
3. **Protected Routes**: Extract JWT → Verify with Supabase JWKS → Decode user info

### Error Handling
- Proper HTTP status codes (400, 401, 403, 500)
- Structured error responses
- Logging for debugging

## Files Created/Modified
- `src/auth_backend/main.py` - FastAPI application
- `src/auth_backend/models.py` - Pydantic models
- `src/auth_backend/auth.py` - Authentication logic
- `src/auth_backend/requirements.txt` - Python dependencies
- `src/auth_backend/Dockerfile` - Container configuration
- `docker-compose.yml` - Add auth-backend service
- `.env.example` - Environment variables
- `tests/test_auth_health.py` - Health check test
- `tests/test_auth_endpoints.py` - Authentication tests