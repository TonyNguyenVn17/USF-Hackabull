# Backend Documentation for Hackathon Website

## Overview
This backend serves the Hackathon website, providing essential functionalities for user management, event handling, and more. It is built using FastAPI and integrates with Firebase for data storage and authentication.

## Tech Stack & Architecture

### Core Technologies
- **FastAPI**: Modern, fast web framework for building APIs with Python
- **Firebase/Firestore**: NoSQL database and backend-as-a-service
- **Python 3.9+**: Core programming language
- **Uvicorn**: ASGI server implementation
- **Pydantic**: Data validation using Python type annotations

### Authentication & Security
- **Firebase Auth**: Multi-provider authentication
- **JWT**: JSON Web Tokens for session management
- **CORS**: Cross-Origin Resource Sharing enabled
- **Environment Variables**: Secure configuration management

### Database Schema
```
users/
  ├── {user_id}/
  │     ├── profile_info
  │     ├── registration_status
  │     └── team_info
  │
teams/
  ├── {team_id}/
  │     ├── team_info
  │     ├── members
  │     └── project_info
  │
events/
  ├── {event_id}/
  │     ├── event_info
  │     ├── attendees
  │     └── check_ins
```

### System Architecture
```
Client <-> FastAPI Server <-> Firebase Services
   ↑            ↑                    ↑
   │            │                    │
   │            │                    ├── Firestore (Database)
   │            │                    ├── Auth (Authentication)
   │            │                    └── Cloud Messaging (Notifications)
   │            │
   │            ├── API Layer (FastAPI)
   │            ├── Business Logic Layer
   │            └── Data Access Layer
   │
   └── Frontend (Next.js)
```

### API Structure
```
/api
  ├── /v1
  │    ├── /auth       # Authentication endpoints
  │    ├── /users      # User management
  │    ├── /teams      # Team operations
  │    ├── /events     # Event management
  │    └── /admin      # Admin operations
  │
  └── /webhooks        # External service webhooks
```

### Performance Optimizations
- Async/await for non-blocking operations
- Firebase batch operations for multiple updates
- Response caching where appropriate
- Background tasks for long-running operations

### Security Measures
- Rate limiting on sensitive endpoints
- Input validation using Pydantic models
- Secure session management
- Role-based access control (RBAC)

## Setup Instructions

### Virtual Environment Setup
We use Python's built-in `venv` module to manage virtual environments:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

# Verify you're in the virtual environment
which python  # Should point to your venv python
```

### Installing Dependencies
We use `requirements.txt` to manage our dependencies:

```bash
# Install all dependencies
pip install -r requirements.txt

# Add new dependencies
pip install package-name
pip freeze > requirements.txt

# Update dependencies
pip install --upgrade -r requirements.txt
```
Remember to always activate your virtual environment before working on the project and deactivate it when you're done:
```bash
# Deactivate the virtual environment when you're done
deactivate
```

## Git Workflow

### Branching Strategy
- **Main**: Production branch
- **Development**: Main branch for ongoing development
- **Feature Branches**: Create feature branches from `development` for new features or bug fixes

### Pulling Updates
To pull the latest changes from the `development` branch, use:
```bash
git pull origin development
```

### Creating a new branch
To create a new feature branch from `development`, use:
```bash
git checkout -b feat/your-feature-name development
```
To create a new testing branch from `development`, use:
```bash
git checkout -b test/your-test-name development
```

## Environment Variables
Ensure environment variables are set correctly:
- Development: Use `.env.local` for local testing
Required variables:
```bash
FIREBASE_CRED_PATH=/path/to/firebase-credentials.json
```

## Running the FastAPI Application
To start the FastAPI application, run:
```bash
cd backend
uvicorn main:app --reload
```

## Testing the API
You can test the new endpoints using curl:
```bash
# Test health check
curl http://localhost:8000/health

# List all users
curl http://localhost:8000/users

# Create a new user
curl -X POST http://localhost:8000/users/test123 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "age": 20
  }'
```

## Deployment

## Features

### Completed Features

#### User Management
- Complete RESTful API for user operations:
  - List users with filters (status, source)
  - Get specific user details
  - Create new users
  - Update user information
  - Delete users
  - Batch import from external sources
- Firebase/Firestore integration for data storage
- Registration status tracking (pending, accepted, rejected, confirmed)

#### Core Infrastructure
- FastAPI backend with async support
- Firebase integration
- CORS enabled for frontend
- Health check endpoints
- Environment variable management
- Dependency management with pip-tools/poetry

#### Data Model
- Comprehensive User model with:
  - Basic info (name, email, age)
  - Academic details (school, major, graduation year)
  - Professional links (GitHub, LinkedIn)
  - Skills and preferences
  - Registration metadata

### Upcoming Features

#### Authentication System
- Multi-provider authentication:
  - Gmail login
  - USF email verification
  - GitHub OAuth
  - Email-password authentication
- JWT-based session management
- Role-based access control

#### Dashboard & Portal
- Application status tracking
- Event information display
- Profile management
- Team formation portal (optional)
- Notification center

#### Event Management
- QR code system:
  - Bulls Connect integration
  - Event check-in
  - Attendance tracking
- Event schedule display
- Real-time updates

#### Communication Features
- Firebase Cloud Messaging:
  - Email notifications
  - Status updates
  - Important announcements
  - Push notifications

#### Security Enhancements (Optional)
- Data encryption
- Rate limiting
- Input validation
- Secure session handling
- API security best practices

#### Admin Features (Optional)
- User management interface
- Event statistics
- Check-in system
- Notification management
- Registration oversight

## Recent Updates (February 2024)
### New RESTful API Endpoints
We've added complete RESTful API endpoints for user management:
- `GET /users`: List all users with optional filters (status, source)
- `GET /users/{user_id}`: Get a specific user
- `POST /users/{user_id}`: Create a new user
- `PUT /users/{user_id}`: Update user details
- `PATCH /users/{user_id}/status`: Update user registration status
- `DELETE /users/{user_id}`: Delete a user
- `POST /users/batch/import`: Batch import users from external sources

