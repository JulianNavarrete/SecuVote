from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.vote_schema import VoteCreate, VoteUpdate, VoteOut
from app.services.vote_service import VoteService
from app.models.vote_model import VoteModel
from pymongo import errors
from uuid import UUID
from app.models.user_model import UserModel
from app.api.deps.user_deps import get_current_user


vote_router = APIRouter()


@vote_router.get("/has-voted", summary="Check if current user has voted in election")
async def has_voted(election_id: str, current_user: UserModel = Depends(get_current_user)):
    try:
        from app.services.vote_service import VoteService
        voted = await VoteService.has_user_voted(current_user.dni, election_id)
        return {"has_voted": voted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@vote_router.post("/create-vote", summary="Create a new vote", response_model=VoteOut)
async def create_vote(
    candidate_id: str,
    election_id: str,
    current_user: UserModel = Depends(get_current_user)
):
    try:
        return await VoteService.create_vote(current_user.dni, candidate_id, election_id)
    except errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vote already registered"
        )


@vote_router.get("/vote/{id}", summary="Get vote details", response_model=VoteOut)
async def get_vote(id: str):
    vote = await VoteService.get_vote_by_id(id)
    if not vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vote not found"
        )
    return vote


@vote_router.get("/", summary="Show all votes", response_model=list[VoteOut])
async def get_votes():
    try:
        return await VoteService.get_votes()
    except errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No votes found"
        )
        




'''
@vote_router.delete("/delete-vote/{id}", summary="Delete Vote")
async def delete_vote(id: str):
    try:
        await VoteService.delete_vote(id)
        return {"detail": "Vote deleted successfully"}
    except errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vote does not exist"
        )


@vote_router.post("/update-vote/{id}", summary="Update Candidate", response_model=CandidateOut)
async def update_candidate(id: str, data: CandidateUpdate):
    try:
        return await CandidateService.update_candidate(id, data)
    except errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidate does not exist"
        )
    

@candidate_router.post("/add-election-to-candidate/{candidate_id}/{election_id}", summary="Add Election to Candidate", response_model=CandidateOut)
async def add_election_to_candidate(candidate_id: str, election_id: str):
    try:
        return await CandidateService.add_election_to_candidate(candidate_id, election_id)
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding the election to the candidate"
        )


@candidate_router.delete("/remove-election-from-candidate/{candidate_id}/{election_id}", summary="Remove Election from Candidate", response_model=CandidateOut)
async def remove_election_from_candidate(candidate_id: str, election_id: str):
    try:
        return await CandidateService.remove_election_from_candidate(candidate_id, election_id)
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while removing the election from the candidate"
        )
'''

