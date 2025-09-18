SecuVote Backend (FastAPI)

Environment variables:
- `JWT_SECRET_KEY`: Secret key for JWT token generation
- `JWT_REFRESH_SECRET_KEY`: Secret key for JWT refresh token generation
- `MONGO_CONNECTION_STRING`: MongoDB connection string
- `BLOCKCHAIN_ENABLED`: Enable/disable blockchain integration (default: True)

Quick installation (Windows):
1. Run `backend/windows-install.ps1`
2. Run `backend/windows-boot.ps1`

Structure:
- `app/app.py`: FastAPI application entry point with MongoDB initialization
- `app/core/`: Configuration and security settings
- `app/models/`: MongoDB document models (User, Election, Candidate, Vote)
- `app/schemas/`: Pydantic schemas for request/response validation
- `app/services/`: Business logic services
- `app/api/api_v1/handlers/`: API route handlers for each entity
- `app/api/auth/`: JWT authentication implementation
- `app/blockchain/`: Algorand blockchain integration

Features:
- FastAPI REST API with automatic OpenAPI documentation
- MongoDB database with Beanie ODM
- JWT-based authentication and authorization
- Blockchain integration with Algorand
- Comprehensive vote management system
- User and candidate management
- Election lifecycle management

API Documentation:
- Interactive docs available at: `http://localhost:8001/api/v1/docs`
- ReDoc documentation at: `http://localhost:8001/api/v1/redoc`
