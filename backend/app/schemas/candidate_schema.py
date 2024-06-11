from pydantic import BaseModel, UUID4, EmailStr, Field
from typing import Optional, List
from uuid import UUID
from beanie import Link, PydanticObjectId
from app.models.election_model import ElectionModel


class CandidateCreate(BaseModel):
    name: str = Field(..., title='Full name', max_length=60, min_length=1, description="Full name of the candidate")
    party: Optional[str] = Field(..., title='Party', max_length=60, min_length=1, description="Party of the candidate")
    bio: Optional[str] = Field(..., title='Biography', max_length=800, min_length=1, description="Biography of the candidate")
    elections: Optional[List[PydanticObjectId]] = None


class CandidateOut(BaseModel):
    candidate_id: str  
    name: str
    party: str
    bio: str
    elections: Optional[List[PydanticObjectId]] = None


class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    party: Optional[str] = None
    bio: Optional[str] = None

