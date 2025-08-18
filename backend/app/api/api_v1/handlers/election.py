from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.candidate_schema import CandidateOut
from app.schemas.election_schema import ElectionCreate, ElectionOut, ElectionUpdate
from app.services.election_service import ElectionService
from app.models.election_model import ElectionModel
from pymongo import errors
from uuid import UUID


election_router = APIRouter()


@election_router.post("/create", summary="Create a new election", response_model=ElectionOut)
async def create_election(data: ElectionCreate):
    try:
        return await ElectionService.create_election(data)
    except errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Election already registered"
        )


@election_router.get("/election/{id}", summary="Get election details", response_model=ElectionOut)
async def get_election(id: str):
    election = await ElectionService.get_election_by_id(id)
    if not election:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Election not found"
        )
    return election


@election_router.get("/elections", summary="Get all elections", response_model=list[ElectionOut])
async def get_all_elections():
    try:
        elections = await ElectionService.get_all_elections()
        return elections
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@election_router.get("/{election_id}/candidates", summary="Get all candidates in an election", response_model=list[CandidateOut])
async def get_election_candidates(election_id: str):
    try:
        return await ElectionService.get_election_candidates(election_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@election_router.post("/update-election/{id}", summary="Update Election", response_model=ElectionOut)
async def update_election(id: str, data: ElectionUpdate):
    try:
        return await ElectionService.update_election(id, data)
    except errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Election does not exist"
        )


@election_router.delete("/delete-election/{id}", summary="Delete Election")
async def delete_election(id: str):
    try:
        await ElectionService.delete_election(id)
        return {"detail": "Election deleted successfully"}
    except errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Election does not exist"
        )


@election_router.post("/add-candidate-to-election/{election_id}/{candidate_id}", summary="Add Candidate to Election", response_model=ElectionOut)
async def add_candidate_to_election(election_id: str, candidate_id: str):
    try:
        return await ElectionService.add_candidate_to_election(election_id, candidate_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@election_router.delete("/remove-candidate-from-election/{election_id}/{candidate_id}", summary="Remove Candidate from Election")
async def remove_candidate_from_election(election_id: str, candidate_id: str):
    try:
        await ElectionService.remove_candidate_from_election(election_id, candidate_id)
        return {"detail": "Candidate removed from election successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

