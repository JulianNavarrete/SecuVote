from app.schemas.candidate_schema import CandidateOut
from app.schemas.election_schema import ElectionCreate, ElectionUpdate, ElectionOut
from app.models.election_model import ElectionModel
from app.models.candidate_model import CandidateModel
from fastapi import HTTPException, status
from typing import Optional, List
from uuid import UUID
from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError
import json
from beanie import Link


class ElectionService:
    @staticmethod
    async def create_election(data: ElectionCreate) -> ElectionModel:
        election = ElectionModel(
            name=data.name,
            description=data.description,
            start_date=data.start_date,
            end_date=data.end_date
        )

        try:
            await election.insert()
            election_out = ElectionOut(
                id=str(election.id),
                name=election.name,
                description=election.description,
                start_date=election.start_date,
                end_date=election.end_date
            )
            return election_out

        except DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Election already registered"
            )
        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


    @staticmethod
    async def get_election_by_id(id: str) -> Optional[ElectionOut]:
        try:
            object_id = ObjectId(id)
            election = await ElectionModel.find_one(ElectionModel.id == object_id)
            if not election:
                return None

            return ElectionOut(
                id=str(election.id),
                name=election.name,
                description=election.description,
                start_date=election.start_date,
                end_date=election.end_date,
                candidates=election.candidates
            )
        except InvalidId:
            return None


    @staticmethod
    async def update_election(id: str, data: ElectionUpdate) -> ElectionOut:
        try:
            object_id = ObjectId(id)
            election = await ElectionModel.find_one(ElectionModel.id == object_id)
            if not election:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Election not found"
                )

            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(election, key, value)
            await election.save()

            return ElectionOut(
                id=str(election.id),
                name=election.name,
                description=election.description,
                start_date=election.start_date,
                end_date=election.end_date,
                candidates=election.candidates
            )
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de elección inválido"
            )


    @staticmethod
    async def delete_election(id: str) -> None:
        try:
            object_id = ObjectId(id)
            election = await ElectionModel.find_one(ElectionModel.id == object_id)
            if not election:
                raise HTTPException(status_code=404, detail="Election not found")
            await election.delete()
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de elección inválido"
            )


    @staticmethod
    async def add_candidate_to_election(election_id: str, candidate_id: str) -> ElectionModel:
        try:
            object_id = ObjectId(election_id)
            election = await ElectionModel.find_one(ElectionModel.id == object_id)
            if not election:
                raise HTTPException(status_code=404, detail="Election not found")

            object_id = ObjectId(candidate_id)
            candidate = await CandidateModel.find_one(CandidateModel.id == object_id)
            if not candidate:
                raise HTTPException(status_code=404, detail="Candidate not found")

            # Create a list of candidates if it does not exist
            if not election.candidates:
                election.candidates = []

            # Check if the candidate is already in the list
            if all(link.ref.id != candidate.id for link in election.candidates):
                election.candidates.append(candidate)
            else:
                raise HTTPException(status_code=400, detail="Candidate already exists in the election's list")

            await election.save()
            election.id = str(election.id)
            return election

        except HTTPException as http_exc:
            # Re-raise HTTPException to avoid capturing it as a 500 error
            raise http_exc

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    

    @staticmethod
    async def remove_candidate_from_election(election_id: str, candidate_id: str) -> ElectionOut:
        try:
            object_id = ObjectId(election_id)
            election = await ElectionModel.find_one(ElectionModel.id == object_id)
            if not election:
                raise HTTPException(status_code=404, detail="Election not found")

            object_id = ObjectId(candidate_id)
            candidate = await CandidateModel.find_one(CandidateModel.id == object_id)
            if not candidate:
                raise HTTPException(status_code=404, detail="Candidate not found")
            
            # Check if the candidate is in the list of candidates
            if not any(link.ref.id == candidate.id for link in election.candidates):
                raise HTTPException(status_code=404, detail="Candidate does not belong to the election")

            # Remove the candidate from the list
            election.candidates = [link for link in election.candidates if link.ref.id != candidate.id]

            await election.save()
            election.id = str(election.id)
            return election
        
        except HTTPException as http_exc:
            # Re-raise HTTPException to avoid capturing it as a 500 error
            raise http_exc

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        

    @staticmethod
    async def get_all_elections():
        elections = await ElectionModel.find_all().to_list()
        # Convertir los elections a ElectionOut explícitamente
        return [
            ElectionOut(
                id=str(election.id),  # Convertir ObjectId a string
                name=election.name,
                description=election.description,
                start_date=election.start_date,
                end_date=election.end_date,
                candidates=election.candidates if hasattr(election, 'candidates') else []
            ) 
            for election in elections
        ]

    @staticmethod
    async def get_election_candidates(election_id: str) -> list[CandidateOut]:
        try:
            object_id = ObjectId(election_id)
            election = await ElectionModel.find_one(ElectionModel.id == object_id)
            
            if not election:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Election not found"
                )

            if not election.candidates:
                return []

            candidates_list = []
            for candidate_link in election.candidates:
                candidate = await CandidateModel.find_one(CandidateModel.id == candidate_link.ref.id)
                if candidate:
                    candidates_list.append(
                        CandidateOut(
                            id=str(candidate.id),
                            name=candidate.name,
                            party=candidate.party,
                            bio=candidate.bio
                        )
                    )

            return candidates_list

        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de elección inválido"
            )
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

