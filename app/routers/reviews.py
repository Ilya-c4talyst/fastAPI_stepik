from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.backend.db_depends import get_db
from sqlalchemy import select, insert, update, func
from app.routers.auth import get_current_user
from app.schemas import CreateReview
from app.models import *

router = APIRouter(prefix='/reviews', tags=['reviews'])


@router.get('/', status_code=200)
async def products_reviews(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_id: int = None
):
    if product_id is not None:
        reviews = await db.scalars(
            select(Review).where(
                Review.product_id == product_id
            )
        )
    else:
        reviews = await db.scalars(
            select(Review)
        )
    if reviews is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no reviews'
        )
    return reviews.all()


@router.post('/', status_code=201)
async def add_review(
    db: Annotated[AsyncSession, Depends(get_db)],
    create_review: CreateReview,
    get_user: Annotated[dict, Depends(get_current_user)]
):
    if get_user.get('id') is not None:

        result = await db.execute(
            insert(Rating).values(
                grade=create_review.rating,
                user_id=get_user.get('user_id'),
                product_id=create_review.product_id,
                is_active=True,
            ).returning(Rating.id) 
        )

        inserted_id = result.scalar()
        await db.commit()

        result = await db.execute(
            select(
                func.avg(Rating.grade)
            ).where(
                Rating.product_id == create_review.product_id,
                Rating.is_active == True,
            )
        )

        average_rating = result.scalar() 

        await db.execute(
            update(Product).where(
                Product.id == create_review.product_id
            ).values(
                rating = average_rating
            )
        )
        await db.commit()


        await db.execute(
            insert(Review).values(
                user_id=get_user.get('id'),
                product_id=create_review.product_id,
                rating_id=inserted_id,
                comment=create_review.comment,
                comment_date=datetime.now(),
                is_active=True
            )
        )

        await db.commit()
        
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You are not authorized to use this method'
        )
    

@router.delete('/', status_code=204)
async def delete_review(
    db: Annotated[AsyncSession, Depends(get_db)],
    review_id: int,
    get_user: Annotated[dict, Depends(get_current_user)]
):
    review_delete = await db.scalar(
        select(Review).where(
            Review.id == review_id
        )
    )
    if review_delete is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There is no review found'
             )
    if get_user.get('is_admin'):
        await db.execute(
            update(Review).where(
                Review.id == review_id
            ).values(
                is_active=False
            )
        )
        await db.commit()
        return {
            'status_code': status.HTTP_204_NO_CONTENT,
            'transaction': 'Product delete is successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You are not have access to this method'
        )