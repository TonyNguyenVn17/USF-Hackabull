# USF-Hackabull

## Overview
This repository hosts the source code for the Hackathon Website, featuring a frontend built with Next.js and a backend using FastAPI integrated with Firebase. 

## Quick Start

1. **Clone the repository**:
   ```
   git clone https://github.com/TonyNguyenVn17/USF-Hackabull.git
   ```
2. **Navigate to the project folder**:
   ```
   cd USF-Hackabull
   cd frontend or backend
   ```

## Backend Overview

- **Framework**: FastAPI
- **Database**: Firestore
- **Authentication**: Supports Gmail, GitHub, USF emails, and standard logins.
- **Features**: User management, QR code integration, notifications via Firebase Cloud Messaging.
- **Security**: Implements robust security measures for data protection and secure API endpoints.

### Setup Instructions

1. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unix/MacOS
   venv\Scripts\activate  # Windows
   ```
2. **Install dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. **Set environment variables**:
   Copy `.env.example` to `.env` and adjust the settings.

4. **Run the backend server**:
   ```bash
   uvicorn backend.app.main:app --reload
   ```

## Contributing

Contributions are welcome! Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
