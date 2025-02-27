# Backend Documentation for Hackathon Website

## Features
- **User Authentication & Management**:
  - RESTful API for user management (CRUD operations)
  - Firebase integration for data storage
  - Registration status tracking (pending, accepted, rejected, confirmed)
  - Batch import support for external registrations

- **Database Operations**: 
  - Firestore integration for scalable data management
  - Real-time data synchronization
  - Secure data access and updates

- **API Endpoints**:
  - Health check and system status
  - User management endpoints
  - Batch operations support
  - CORS enabled for frontend integration

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

### Enhanced User Model
The User model now includes additional fields for hackathon registration:
```python
class User(BaseModel):
    name: str
    email: str
    age: int
    school: Optional[str]
    major: Optional[str]
    graduation_year: Optional[int]
    github: Optional[str]
    linkedin: Optional[str]
    skills: Optional[List[str]]
    dietary_restrictions: Optional[str]
    shirt_size: Optional[str]
    team_id: Optional[str]
    registration_status: str  # pending, accepted, rejected, confirmed
    registration_source: str  # direct, google_form, airtable
    created_at: datetime
    updated_at: datetime
```

## Setup Instructions

### Virtual Environment
Create and activate a virtual environment to manage Python dependencies:

```bash
# Create environment
python -m venv venv

# Activate environment
source venv/bin/activate  # Unix/MacOS
venv\Scripts\activate  # Windows
```

### Managing Dependencies with `pip-tools`
This project uses `pip-tools` to manage dependencies efficiently and ensure reproducibility. Instead of editing `requirements.txt` directly, we define dependencies in `requirements.in` and use `pip-compile` to generate a locked requirements file.

#### **Install `pip-tools`**
```bash
pip install pip-tools
```

#### **Define dependencies**
Instead of modifying `requirements.txt`, list top-level dependencies in `requirements.in`:
```txt
Flask
firebase-admin
requests
```

#### **Compile dependencies**
Use `pip-compile` to resolve and generate a locked `requirements.txt` file:
```bash
pip-compile requirements.in
```
This outputs a `requirements.txt` file with all pinned dependencies and versions.

#### **Install dependencies**
To install dependencies from the compiled `requirements.txt`, run:
```bash
pip install -r requirements.txt
```

### Using `pyproject.toml` for Dependency Management
Instead of `requirements.in`, the project can also use `pyproject.toml` for managing dependencies in modern Python workflows. The `pyproject.toml` file contains project metadata and dependencies.

Example `pyproject.toml`:
```toml
[tool.poetry]
name = "hackathon-backend"
version = "0.1.0"
description = "Backend for the Hackathon website"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.8"
Flask = "^2.0"
firebase-admin = "^5.0"
requests = "^2.26"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

To install dependencies using `pyproject.toml`, run:
```bash
poetry install
```

If switching between `pip-tools` and `poetry`, ensure the dependency management method remains consistent.

## Git Workflow

### Branching Strategy
- **Main**: Production branch
- **Development**: Main branch for ongoing development
- **Feature Branches**: Create feature branches from `development` for new features or bug fixes
  - Current feature branches:
    - `feature/user-rest-api`: User management REST API implementation

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

## Coming Soon

### Authentication & Authorization
- JWT-based authentication system
- Multi-provider authentication:
  - Gmail integration
  - USF email verification
  - GitHub OAuth
  - Custom email-password authentication
- Role-based access control (Individual, Team, Organizer)

### User Management
- Enhanced profile management
- Team features:
  - Team creation and management
  - Team matching system
  - Team size restrictions and validation
- Unique username enforcement
- Password security and recovery system

### Event Management
- QR code integration:
  - Bulls Connect QR integration
  - Auto-generated unique QR codes
  - Check-in system
  - Event attendance tracking
- Project submission system:
  - Devpost integration
  - Project documentation
  - Team submission validation

### Communication System 
- Firebase Cloud Messaging integration:
  - Real-time notifications
  - Email notifications
  - Important announcements
  - Status update notifications
  - Push notifications

### Security Features
- Data encryption
- Secure authentication flows
- Rate limiting
- Input validation and sanitization

### Admin Dashboard (Optional)
- User management interface
- Event statistics
- Check-in management
- Notification management

