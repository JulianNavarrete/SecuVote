from app.schemas.candidate_schema import CandidateCreate, CandidateUpdate, CandidateOut
from app.models.candidate_model import CandidateModel
from app.models.election_model import ElectionModel
from fastapi import HTTPException, status
from typing import Optional
from uuid import UUID
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from beanie import Link
import json
from algosdk import account, mnemonic


class CandidateService:
    @staticmethod
    async def create_candidate(data: CandidateCreate) -> CandidateModel:
        existing_candidate = await CandidateModel.find_one(CandidateModel.name == data.name)
        if existing_candidate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un candidato con el nombre '{data.name}'"
            )

        candidate = CandidateModel(
            name=data.name,
            party=data.party,
            bio=data.bio,
            algorand_address=None,
            algorand_mnemonic=None,
            algorand_private_key=None
        )

        # Generate an address, mnemonic key and private key for the new candidate
        new_address = account.generate_account()
        candidate.algorand_private_key = new_address[0]
        candidate.algorand_address = new_address[1]
        candidate.algorand_mnemonic = mnemonic.from_private_key(new_address[0])


        try:
            await candidate.insert()
            candidate_out = CandidateOut(
                id=str(candidate.id),
                name=candidate.name,
                party=candidate.party,
                bio=candidate.bio,
                algorand_address=candidate.algorand_address,
                algorand_mnemonic=candidate.algorand_mnemonic,
                algorand_private_key=candidate.algorand_private_key
            )
            return candidate_out
        
        except DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Candidate already registered"
            )
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
    async def get_candidate_by_name(name: str) -> Optional[CandidateOut]:
        candidate = await CandidateModel.find_one(CandidateModel.name == name)
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


    @staticmethod
    async def add_election_to_candidate(candidate_id: str, election_id: str) -> CandidateOut:
        try:
            object_id = ObjectId(candidate_id)
            candidate = await CandidateModel.find_one(CandidateModel.id == object_id)
            if not candidate:
                raise HTTPException(status_code=404, detail="Candidate not found")

            object_id = ObjectId(election_id)            
            election = await ElectionModel.find_one(ElectionModel.id == object_id)
            if not election:
                raise HTTPException(status_code=404, detail="Election not found")

            # Create an empty list if it does not exist
            if not candidate.elections:
                candidate.elections = []

            # Check if the election is already in the list of elections
            if all(link.ref.id != election.id for link in candidate.elections):
                candidate.elections.append(election)
            else:
                raise HTTPException(status_code=400, detail="Election already exists in the candidate's list")

            await candidate.save()
            candidate.id = str(candidate.id)
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
    async def remove_election_from_candidate(candidate_id: str, election_id: str) -> CandidateOut:
        try:
            object_id = ObjectId(candidate_id)
            candidate = await CandidateModel.find_one(CandidateModel.id == object_id)
            if not candidate:
                raise HTTPException(status_code=404, detail="Candidate not found")

            object_id = ObjectId(election_id)
            election = await ElectionModel.find_one(ElectionModel.id == object_id)
            if not election:
                raise HTTPException(status_code=404, detail="Election not found")
            
            # Check if the election is in the list of elections
            if not any(link.ref.id == election.id for link in candidate.elections):
                raise HTTPException(status_code=404, detail="Election does not belong to the candidate")

            # Remove the election from the list
            candidate.elections = [link for link in candidate.elections if link.ref.id != election.id]

            await candidate.save()
            candidate.id = str(candidate.id)
            return candidate
        
        except HTTPException as http_exc:
            # Re-raise HTTPException to avoid capturing it as a 500 error
            raise http_exc

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

