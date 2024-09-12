from pydantic import BaseModel, UUID4, EmailStr, Field
from typing import Optional, List
from uuid import UUID
from app.models.election_model import ElectionModel


class CandidateCreate(BaseModel):
    name: str = Field(..., title='Full name', max_length=60, min_length=1, description="Full name of the candidate")
    party: Optional[str] = Field(..., title='Party', max_length=60, min_length=1, description="Party of the candidate")
    bio: Optional[str] = Field(..., title='Biography', max_length=800, min_length=1, description="Biography of the candidate")


class CandidateOut(BaseModel):
    id: str
    name: str
    party: str
    bio: str


class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    party: Optional[str] = None
    bio: Optional[str] = None
    algorand_address: Optional[str]
    algorand_mnemonic: Optional[str]
    # algorand_private_key: Optional[str]



class CandidateOutVote(BaseModel):
    id: str
    name: str
    party: str
    algorand_address: Optional[str]
    algorand_mnemonic: Optional[str]
    # algorand_private_key: Optional[str]

