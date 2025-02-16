from typing import Optional
import os
import logging
from functools import lru_cache

import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
from pathlib import Path

logger = logging.getLogger(__name__)

class FirebaseConfig:
    _instance = None
    _db = None

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
                env_path = Path(__file__).parent.parent / '.env.local'
                load_dotenv(dotenv_path=env_path)
                
                cred_path = os.getenv("FIREBASE_CRED_PATH")
                if not cred_path:
                    raise ValueError("FIREBASE_CRED_PATH not set in environment variables")
                
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