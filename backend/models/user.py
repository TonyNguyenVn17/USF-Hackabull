from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    name: str
    email: str
    age: int
    school: Optional[str] = None
    major: Optional[str] = None
    graduation_year: Optional[int] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    skills: Optional[List[str]] = []
    dietary_restrictions: Optional[str] = None
    shirt_size: Optional[str] = None
    team_id: Optional[str] = None
    registration_status: str = Field(default="pending", description="pending, accepted, rejected, confirmed")
    registration_source: str = Field(default="direct", description="direct, google_form, airtable")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now) 