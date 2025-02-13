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

### Install Dependencies
Install necessary dependencies from the requirements file:

```bash
pip install -r requirements.txt
```

### Environment Variables
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