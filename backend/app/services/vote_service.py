from app.schemas.vote_schema import VoteOut
from app.models.candidate_model import CandidateModel
from app.models.election_model import ElectionModel
from app.models.user_model import UserModel
from app.models.vote_model import VoteModel
from app.schemas.candidate_schema import CandidateOutVote
from app.schemas.election_schema import ElectionOutVote
from app.schemas.user_schema import UserOutVote
from fastapi import HTTPException, status
from typing import Optional
from uuid import UUID
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from beanie import Link
import json


class VoteService:
    @staticmethod
    async def create_candidate(user_id: str, str,candidate_id: str, election_id: str) -> VoteModel:
        try:
            object_id = ObjectId(user_id)
            user = await UserModel.find_one(UserModel.id == object_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            user = UserOutVote(
                id=ObjectId(user_id),
                dni=user.dni,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name
            )
            
            object_id = ObjectId(candidate_id)
            candidate = await CandidateModel.find_one(CandidateModel.id == object_id)
            if not candidate:
                raise HTTPException(status_code=404, detail="Candidate not found")
            
            candidate = CandidateOutVote(
                id=ObjectId(candidate_id),
                name=candidate.name,
                party=candidate.party,
            )

            object_id = ObjectId(election_id)            
            election = await ElectionModel.find_one(ElectionModel.id == object_id)
            if not election:
                raise HTTPException(status_code=404, detail="Election not found")
            
            election = ElectionOutVote(
                id=ObjectId(election_id),
                name=election.name,
                description=election.description,
            )







            if all(link.ref.id != user.id for link in user.id):
                vote.voter.save(user)
            else:
                raise HTTPException(status_code=400, detail="Election already exists in the candidate's list")

            if all(link.ref.id != election.id for link in candidate.elections):
                candidate.elections.append(election)
            else:
                raise HTTPException(status_code=400, detail="Election already exists in the candidate's list")
            


            await vote.save()
            # candidate.id = str(candidate.id)
            return candidate


            
        except HTTPException as http_exc:
            # Re-raise HTTPException to avoid capturing it as a 500 error
            raise http_exc
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )









    @staticmethod
    async def get_candidate_by_id(id: str) -> Optional[CandidateOut]:
        object_id = ObjectId(id)
        candidate = await CandidateModel.find_one(CandidateModel.id == object_id)
        if not candidate:
            return None

        return CandidateOut(
            id=str(candidate.id),
            name=candidate.name,
            party=candidate.party,
            bio=candidate.bio,
            election_id=candidate.elections
        )


    @staticmethod
    async def update_candidate(id: str, data: CandidateUpdate) -> CandidateOut:
        object_id = ObjectId(id)
        candidate = await CandidateModel.find_one(CandidateModel.id == object_id)
        if not candidate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate not found"
            )

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(candidate, key, value)
        await candidate.save()

        return CandidateOut(
            id=str(candidate.id),
            name=candidate.name,
            party=candidate.party,
            bio=candidate.bio,
            election_id=candidate.elections
        )


    @staticmethod
    async def delete_candidate(id: str) -> None:
        object_id = ObjectId(id)
        candidate = await CandidateModel.find_one(CandidateModel.id == object_id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        await candidate.delete()