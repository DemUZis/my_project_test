from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.review import Review
from app.schemes.review import ReviewCreate, ReviewUpdate


class ReviewRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, review_data: ReviewCreate) -> Review:
        review = Review(
            client_id=review_data.client_id,
            master_id=review_data.master_id,
            appointment_id=review_data.appointment_id,
            rating=review_data.rating,
            comment=review_data.comment
        )
        self.db_session.add(review)
        await self.db_session.commit()
        await self.db_session.refresh(review)
        return review

    async def get_by_id(self, review_id: int) -> Optional[Review]:
        result = await self.db_session.execute(
            select(Review)
            .options(selectinload(Review.client))
            .options(selectinload(Review.master))
            .options(selectinload(Review.appointment))
            .where(Review.id == review_id)
        )
        return result.scalar_one_or_none()

    async def get_by_master_id(self, master_id: int) -> List[Review]:
        result = await self.db_session.execute(
            select(Review)
            .options(selectinload(Review.client))
            .options(selectinload(Review.appointment))
            .where(Review.master_id == master_id)
        )
        return result.scalars().all()

    async def get_by_client_id(self, client_id: int) -> List[Review]:
        result = await self.db_session.execute(
            select(Review)
            .options(selectinload(Review.master))
            .options(selectinload(Review.appointment))
            .where(Review.client_id == client_id)
        )
        return result.scalars().all()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Review]:
        result = await self.db_session.execute(
            select(Review)
            .options(selectinload(Review.client))
            .options(selectinload(Review.master))
            .options(selectinload(Review.appointment))
            .offset(skip)
            .limit(limit)
            .order_by(Review.id)
        )
        return result.scalars().all()

    async def update(self, review_id: int, review_data: ReviewUpdate) -> Optional[Review]:
        review = await self.get_by_id(review_id)
        if review:
            for field, value in review_data.dict(exclude_unset=True).items():
                setattr(review, field, value)
            await self.db_session.commit()
            await self.db_session.refresh(review)
        return review

    async def delete(self, review_id: int) -> bool:
        review = await self.get_by_id(review_id)
        if review:
            await self.db_session.delete(review)
            await self.db_session.commit()
            return True
        return False