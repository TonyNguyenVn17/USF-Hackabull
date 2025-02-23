# Backend Documentation for Hackathon Website

## Features
- **User Authentication**: Supports Gmail, GitHub, USF emails, and traditional registration methods.
- **Database Operations**: Manages dynamic CRUD operations using Firestore.
- **Notifications**: Utilizes Firebase Cloud Messaging for prompt user notifications.
- **QR Code Processing**: Facilitates event logistics through QR code generation and scanning.

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

## Environment Variables
Ensure environment variables are set correctly:
- Development: Use `.env.local` for local testing.
- Production: Switch to `.env.production` for deployment settings.

## Running Firebase Tests
Test Firebase integration to verify setup and functionality:

1. **Navigate** to the Firebase test directory:
   ```bash
   cd app/firebase_test/
   ```
2. **Run the test script**:
   ```bash
   python3 test_firebase.py
   ```

This will check Firestore connectivity and operations, with editable test parameters located in `test_firebase.py`.

## Deployment

