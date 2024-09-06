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
from datetime import datetime as dt, UTC
from app.blockchain.algorand import send_algorand_txn, sign_algorand_txn, create_algorand_txn, algod_client
from algosdk.error import AlgodHTTPError


class VoteService:
    @staticmethod
    async def create_vote(dni: int, candidate_id: str, election_id: str) -> VoteOut:
        try:
            existing_vote = await VoteModel.find_one(
                VoteModel.voter.dni == dni,
                VoteModel.election.id == election_id
            )

            if existing_vote:
                raise HTTPException(status_code=400, detail="User has already voted in this election")

            user = await UserModel.find_one(UserModel.dni == dni)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            user = UserOutVote(
                id=str(user.id),
                dni=user.dni,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                algorand_address=user.algorand_address,
                algorand_mnemonic=user.algorand_mnemonic,
                algorand_private_key=user.algorand_private_key
            )
            
            object_id = ObjectId(election_id)            
            election = await ElectionModel.find_one(ElectionModel.id == object_id)
            if not election:
                raise HTTPException(status_code=404, detail="Election not found")
            
            election = ElectionOutVote(
                id=election_id,
                name=election.name,
                description=election.description,
            )

            object_id = ObjectId(candidate_id)
            candidate = await CandidateModel.find_one(CandidateModel.id == object_id)
            if not candidate:
                raise HTTPException(status_code=404, detail="Candidate not found")

            candidate = CandidateOutVote(
                id=candidate_id,
                name=candidate.name,
                party=candidate.party,
                algorand_address=candidate.algorand_address,
                algorand_mnemonic=candidate.algorand_mnemonic,
                algorand_private_key=candidate.algorand_private_key
            )


            try:
                sender_mnemonic = user.algorand_mnemonic
                
                # Goes to a government account
                # algo_txn = create_algorand_txn(user.algorand_address, 'QRFW3WKHHOVO6I2VJXMJKQXQTHBXLION3EKAGQF4CWKUKDF4CZMVDLMG5Q')
                
                # Goes to candidate account (still testing)
                algo_txn = create_algorand_txn(user.algorand_address, candidate.algorand_address)
                
                signed_txn = sign_algorand_txn(algo_txn, sender_mnemonic)
            except AlgodHTTPError as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"AlgodHTTPError: {str(e)}"
            )

            txid = send_algorand_txn(signed_txn)

            # Create vote
            vote = VoteModel(
                voter=user.model_dump(),
                candidate=candidate.model_dump(),
                election=election.model_dump(),
                timestamp=dt.now(UTC),
                transaction_id_algorand=txid
            )

            # Save vote to database
            await vote.save()

            vote_out = VoteOut(
                id=str(vote.id),
                voter=str(vote.voter["id"]), 
                candidate=str(vote.candidate["id"]), 
                election=str(vote.election["id"]), 
                timestamp=vote.timestamp,
                transaction_id_algorand=txid
            )
            return vote_out

    
        except HTTPException as http_exc:
            # Re-raise HTTPException to avoid capturing it as a 500 error
            raise http_exc
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


    @staticmethod
    async def get_vote_by_id(id: str) -> Optional[VoteModel]:
        try:
            object_id = ObjectId(id)
            vote = await VoteModel.find_one(VoteModel.id == object_id)
            if not vote:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Vote not found"
                )

            vote_out = VoteOut(
                id=str(vote.id),
                voter=str(vote.voter["dni"]), 
                candidate=str(vote.candidate["name"]), 
                election=str(vote.election["name"]), 
                timestamp=vote.timestamp,
                transaction_id_algorand=vote.transaction_id_algorand
            )
            return vote_out

        except HTTPException as http_exc:
            # Re-raise HTTPException to avoid capturing it as a 500 error
            raise http_exc

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


    @staticmethod
    async def get_votes() -> list[VoteOut]:
        try:
            votes = await VoteModel.all().to_list()
            return [
                VoteOut(
                    id=str(vote.id),
                    voter=str(vote.voter["id"]), 
                    candidate=str(vote.candidate["id"]), 
                    election=str(vote.election["id"]), 
                    timestamp=vote.timestamp,
                    transaction_id_algorand=vote.transaction_id_algorand
                )
                for vote in votes
            ]
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

