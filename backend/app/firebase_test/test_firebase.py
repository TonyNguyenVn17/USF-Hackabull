import os
import logging
from typing import Dict, Optional

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FirestoreManager:
    def __init__(self, env_path: str = "../../.env.local"):
        # Initialize FirestoreManager with Firebase credentials.
        self.db = self._initialize_firebase(env_path)

    def _initialize_firebase(self, env_path: str) -> firestore.Client:
        try:
            load_dotenv(dotenv_path=env_path)
            service_account_path = os.getenv("FIREBASE_CRED_PATH")

            if not service_account_path:
                raise ValueError("FIREBASE_CRED_PATH environment variable is not set.")

            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
            return firestore.client()
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")
            raise

    def write_document(self, collection: str, document: str, data: Dict) -> bool:
        try:
            self.db.collection(collection).document(document).set(data)
            logger.info(f"Successfully wrote to {collection}/{document}")
            return True
        except Exception as e:
            logger.error(f"Error writing document: {e}")
            return False

    def read_document(self, collection: str, document: str) -> Optional[Dict]:
        try:
            doc_ref = self.db.collection(collection).document(document).get()
            if doc_ref.exists:
                logger.info(f"Successfully read from {collection}/{document}")
                return doc_ref.to_dict()
            logger.warning(f"No document found at {collection}/{document}")
            return None
        except Exception as e:
            logger.error(f"Error reading document: {e}")
            return None


def test_firestore():
    # Test Firestore read and write operations.
    try:
        firestore_manager = FirestoreManager()
        test_data = {
                    "hello": "world",
                    "test": "firebase"
                    }

        # Test write
        write_success = firestore_manager.write_document(
            "testCollection", "testDoc", test_data
        )

        # Test read
        if write_success:
            result = firestore_manager.read_document("testCollection", "testDoc")
            if result:
                logger.info(f"Read data: {result}")
    except Exception as e:
        logger.error(f"Test failed: {e}")


if __name__ == "__main__":
    test_firestore()
