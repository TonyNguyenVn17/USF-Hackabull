from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from typing import Dict, Any, List, Optional
from models.user import User
from core.firebase_config import FirebaseConfig
from datetime import datetime

router = APIRouter()
firebase = FirebaseConfig()

@router.get("/")
async def list_users(
    status: Optional[str] = Query(None, description="Filter by registration status"),
    source: Optional[str] = Query(None, description="Filter by registration source")
):
    """List all users from Firebase with optional filters"""
    try:
        users = await firebase.get_collection("users")
        if users is None:
            return {"message": "No users found", "data": []}
        
        # Apply filters if provided
        filtered_users = users
        if status:
            filtered_users = {k: v for k, v in filtered_users.items() if v.get('registration_status') == status}
        if source:
            filtered_users = {k: v for k, v in filtered_users.items() if v.get('registration_source') == source}
            
        return {"message": "Users retrieved successfully", "data": filtered_users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
async def get_user(user_id: str):
    """Get a specific user by ID"""
    try:
        user = await firebase.get_document("users", user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User retrieved successfully", "data": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{user_id}")
async def create_user(user_id: str, user: User):
    """Create a new user"""
    try:
        # Check if user already exists
        existing_user = await firebase.get_document("users", user_id)
        if existing_user:
            raise HTTPException(status_code=400, detail="User ID already exists")
        
        success = await firebase.set_document("users", user_id, user.model_dump())
        if not success:
            raise HTTPException(status_code=500, detail="Failed to create user")
        return {"message": f"User {user_id} created successfully", "data": user}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{user_id}")
async def update_user(user_id: str, user: User):
    """Update an existing user"""
    try:
        existing_user = await firebase.get_document("users", user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update the timestamp
        user_data = user.model_dump()
        user_data["updated_at"] = datetime.now()
        
        success = await firebase.set_document("users", user_id, user_data)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update user")
        return {"message": f"User {user_id} updated successfully", "data": user_data}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{user_id}/status")
async def update_user_status(
    user_id: str, 
    status: str = Query(..., description="New registration status (pending, accepted, rejected, confirmed)")
):
    """Update user's registration status"""
    try:
        existing_user = await firebase.get_document("users", user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if status not in ["pending", "accepted", "rejected", "confirmed"]:
            raise HTTPException(status_code=400, detail="Invalid status value")
        
        existing_user["registration_status"] = status
        existing_user["updated_at"] = datetime.now()
        
        success = await firebase.set_document("users", user_id, existing_user)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update user status")
        return {"message": f"User {user_id} status updated to {status}", "data": existing_user}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch/import")
async def import_users(users: List[User]):
    """Batch import users from external sources (Google Form/Airtable)"""
    try:
        results = []
        for user in users:
            # Generate a user_id from email (you might want to use a different strategy)
            user_id = user.email.split('@')[0]
            # Set import metadata
            user_data = user.model_dump()
            user_data["registration_source"] = "external"
            
            success = await firebase.set_document("users", user_id, user_data)
            results.append({
                "user_id": user_id,
                "email": user.email,
                "success": success
            })
        
        return {
            "message": "Batch import completed",
            "data": {
                "total": len(users),
                "results": results
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    """Delete a user"""
    try:
        existing_user = await firebase.get_document("users", user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        success = await firebase.delete_document("users", user_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete user")
        return {"message": f"User {user_id} deleted successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync/google-form")
async def sync_form_responses(
    background_tasks: BackgroundTasks,
    spreadsheet_id: str = Query(..., description="Google Sheets ID from the form responses spreadsheet"),
    range_name: str = Query("Form Responses 1!A:Z", description="Sheet range to read")
):
    """Sync responses from Google Form to Firebase"""
    try:
        # Run sync in background to avoid timeout
        background_tasks.add_task(firebase.sync_form_responses, spreadsheet_id, range_name)
        return {
            "message": "Form sync started in background",
            "status": "processing"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 