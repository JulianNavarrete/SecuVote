from beanie import Document, Link, Indexed
import datetime as dt
from typing import Optional, List


class ElectionModel(Document):
    # election_id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    start_date: Optional[dt.datetime] = None
    end_date: Optional[dt.datetime] = None
    candidates: Optional[List[Link["CandidateModel"]]] = None


    def __repr__(self) -> str:
        return f"<Election {self.name}>"


    class Settings:
        name = "elections"


from app.models.candidate_model import CandidateModel
