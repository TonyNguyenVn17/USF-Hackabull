from typing import Optional
import os
import logging
from functools import lru_cache
import json

import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

class FirebaseConfig:
    _instance = None
    _db = None
    _sheets_service = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    @lru_cache()
    def initialize_firebase():
        """Initialize Firebase connection if not already initialized"""
        if not firebase_admin._apps:
            try:
                # Get the absolute path to .env.local
                env_path = Path(__file__).parent.parent / ".env.local"
                load_dotenv(dotenv_path=env_path)

                cred_path = os.getenv("FIREBASE_CRED_PATH")
                if not cred_path:
                    raise ValueError(
                        "FIREBASE_CRED_PATH not set in environment variables"
                    )

                # Ensure the credential file exists
                if not Path(cred_path).exists():
                    raise ValueError(f"Credential file not found at: {cred_path}")

                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                logger.info("Firebase initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Firebase: {e}")
                raise

    @property
    def sheets_service(self):
        """Get or create Google Sheets service"""
        if not self._sheets_service:
            try:
                creds_path = os.getenv("GOOGLE_CREDS_PATH")
                if not creds_path:
                    raise ValueError("GOOGLE_CREDS_PATH not set in environment variables")

                credentials = service_account.Credentials.from_service_account_file(
                    creds_path, scopes=SCOPES
                )
                self._sheets_service = build('sheets', 'v4', credentials=credentials)
            except Exception as e:
                logger.error(f"Failed to initialize Google Sheets service: {e}")
                raise
        return self._sheets_service

    async def sync_form_responses(self, spreadsheet_id: str, range_name: str) -> bool:
        """Sync Google Form responses to Firebase"""
        try:
            # Get form responses from Google Sheets
            sheet = self.sheets_service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            rows = result.get('values', [])
            if not rows:
                logger.info('No data found in Google Sheet')
                return True

            # First row contains headers
            headers = rows[0]
            
            # Process each response
            for row in rows[1:]:  # Skip header row
                # Create a dictionary from the row data
                user_data = {}
                for i, value in enumerate(row):
                    if i < len(headers):  # Ensure we have a header for this column
                        key = headers[i].lower().replace(' ', '_')
                        user_data[key] = value

                # Map Google Form fields to our User model
                user = {
                    "name": user_data.get('full_name', ''),
                    "email": user_data.get('email', ''),
                    "age": int(user_data.get('age', 0)),
                    "school": user_data.get('school', ''),
                    "major": user_data.get('major', ''),
                    "graduation_year": int(user_data.get('graduation_year', 0)),
                    "github": user_data.get('github_profile', ''),
                    "linkedin": user_data.get('linkedin_profile', ''),
                    "skills": user_data.get('skills', '').split(','),
                    "dietary_restrictions": user_data.get('dietary_restrictions', ''),
                    "shirt_size": user_data.get('shirt_size', ''),
                    "registration_source": "google_form",
                    "registration_status": "pending"
                }

                # Use email as user_id (you might want a different strategy)
                user_id = user['email'].split('@')[0]
                
                # Check if user already exists
                existing_user = await self.get_document("users", user_id)
                if not existing_user:
                    await self.set_document("users", user_id, user)
                    logger.info(f"Imported user from form: {user_id}")

            return True
        except Exception as e:
            logger.error(f"Error syncing form responses: {e}")
            return False

    @property
    def db(self) -> firestore.Client:
        """Get Firestore client instance"""
        if not self._db:
            self.initialize_firebase()
            self._db = firestore.client()
        return self._db

    async def get_document(self, collection: str, document_id: str) -> Optional[dict]:
        """Async method to get a document from Firestore"""
        try:
            doc_ref = self.db.collection(collection).document(document_id).get()
            return doc_ref.to_dict() if doc_ref.exists else None
        except Exception as e:
            logger.error(f"Error getting document: {e}")
            return None

    async def set_document(self, collection: str, document_id: str, data: dict) -> bool:
        """Async method to set a document in Firestore"""
        try:
            self.db.collection(collection).document(document_id).set(data)
            logger.info(f"Successfully wrote to {collection}/{document_id}")
            return True
        except Exception as e:
            logger.error(f"Error setting document: {e}")
            return False

    async def get_collection(self, collection: str) -> Optional[dict]:
        """Async method to get all documents from a collection"""
        try:
            docs = self.db.collection(collection).stream()
            documents = {}
            for doc in docs:
                documents[doc.id] = doc.to_dict()
            logger.info(f"Successfully retrieved collection {collection}")
            return documents
        except Exception as e:
            logger.error(f"Error getting collection: {e}")
            return None

    async def delete_document(self, collection: str, document_id: str) -> bool:
        """Async method to delete a document from Firestore"""
        try:
            self.db.collection(collection).document(document_id).delete()
            logger.info(f"Successfully deleted {collection}/{document_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False
