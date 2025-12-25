from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.database import async_session_maker
from app.repositories.review import ReviewRepository
from app.repositories.appointment import AppointmentRepository
from app.schemes.review import ReviewCreate, ReviewUpdate, ReviewInDB
from app.schemes.user import UserInDB
from app.dependencies import get_current_user


router = APIRouter(prefix="/reviews", tags=["reviews"])


async def get_db():
    async with async_session_maker() as session:
        yield session


@router.post("/", response_model=ReviewInDB)
async def create_review(
    review: ReviewCreate,
    current_user: UserInDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    review_repository = ReviewRepository(db)
    
    # Ensure the client can only create reviews for themselves
    if review.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create review for another user"
        )
    
    # Verify that the appointment belongs to the current user
    appointment_repository = AppointmentRepository(db)
    appointment = await appointment_repository.get_by_id(review.appointment_id)
    
    if not appointment or appointment.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create review for an appointment that doesn't belong to you"
        )
    
    db_review = await review_repository.create(review)
    return db_review


@router.get("/{review_id}", response_model=ReviewInDB)
async def get_review(
    review_id: int,
    current_user: UserInDB = Depends(get_current_user),
    review_repository: ReviewRepository = Depends(lambda: ReviewRepository(next(get_db())))
):
    review = await review_repository.get_by_id(review_id)
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    # Only allow the review owner or admin to view the review
    if review.client_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this review"
        )
    
    return review


@router.put("/{review_id}", response_model=ReviewInDB)
async def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    current_user: UserInDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    review_repository = ReviewRepository(db)
    review = await review_repository.get_by_id(review_id)
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    # Only allow the review owner to update the review
    if review.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this review"
        )
    
    updated_review = await review_repository.update(review_id, review_update)
    return updated_review


@router.delete("/{review_id}")
async def delete_review(
    review_id: int,
    current_user: UserInDB = Depends(get_current_user),
    review_repository: ReviewRepository = Depends(lambda: ReviewRepository(next(get_db())))
):
    review = await review_repository.get_by_id(review_id)
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    # Only allow the review owner or admin to delete the review
    if review.client_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this review"
        )
    
    success = await review_repository.delete(review_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    return {"message": "Review deleted successfully"}


@router.get("/master/{master_id}", response_model=List[ReviewInDB])
async def get_reviews_by_master(
    master_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: UserInDB = Depends(get_current_user),
    review_repository: ReviewRepository = Depends(lambda: ReviewRepository(next(get_db())))
):
    # Anyone can view reviews for a master
    reviews = await review_repository.get_by_master_id(master_id)
    return reviews


@router.get("/client/{client_id}", response_model=List[ReviewInDB])
async def get_reviews_by_client(
    client_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: UserInDB = Depends(get_current_user),
    review_repository: ReviewRepository = Depends(lambda: ReviewRepository(next(get_db())))
):
    # Only allow the client themselves or an admin to view their reviews
    if current_user.id != client_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these reviews"
        )
    
    reviews = await review_repository.get_by_client_id(client_id)
    return reviews