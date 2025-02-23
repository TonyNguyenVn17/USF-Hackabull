from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.firebase_config import FirebaseConfig
from pydantic import BaseModel

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase
firebase = FirebaseConfig()


class User(BaseModel):
    name: str
    email: str
    age: int


@app.get("/")
async def root():
    return {"message": "Welcome to Hackabull API"}


@app.post("/users/{user_id}")
async def create_user(user_id: str, user: User):
    """Create a new user in Firebase"""
    try:
        print(f"Attempting to create user {user_id} with data: {user.model_dump()}")  # Debug print
        success = await firebase.set_document("users", user_id, user.model_dump())
        if not success:
            print("Firebase operation failed")  # Debug print
            raise HTTPException(status_code=500, detail="Failed to create user")
        return {"message": f"User {user_id} created successfully", "data": user}
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug print
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """Get a user from Firebase"""
    try:
        result = await firebase.get_document("users", user_id)
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User found", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test-firebase")
async def test_firebase():
    """Test endpoint to verify Firebase connection"""
    try:
        # Test writing to Firestore
        test_data = {"test": "data"}
        success = await firebase.set_document("test", "test-doc", test_data)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to write to Firestore")

        # Test reading from Firestore
        result = await firebase.get_document("test", "test-doc")
        if result is None:
            raise HTTPException(status_code=404, detail="Document not found")

        return {"message": "Firebase connection successful", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Add more routes here as needed
