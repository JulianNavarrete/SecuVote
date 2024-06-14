from pydantic import BaseModel, Field
from beanie import Link
from app.models.candidate_model import CandidateModel
from app.models.election_model import ElectionModel
from app.models.user_model import UserModel
from datetime import datetime, UTC


class VoteCreate(BaseModel):
    transaction_id_algorand: str


class VoteUpdate(BaseModel):
    pass


class VoteOut(BaseModel):
    id: str
    voter: str
    candidate: str
    election: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    transaction_id_algorand: str

