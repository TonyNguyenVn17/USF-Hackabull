from typing import List, Optional
from pydantic import BaseModel

class Team(BaseModel):
    name: str
    members: List[str]
    project_name: Optional[str] = None
    project_description: Optional[str] = None
    tech_stack: List[str] = [] 