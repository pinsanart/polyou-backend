from fastapi import APIRouter, Depends, Query
from typing import Annotated
from sqlalchemy.orm import Session

from ..schemas.user import UserIdentity
from ..schemas.flashcards import FlashcardCreate, FlashcardTypes, RatingEnum
from ..db.session import get_db
from ..dependencies.auth import get_active_user
from ..db.crud.flashcards import (
    get_all_flashcards_by_user_id, 
    create_flashcard,
    get_flashcards_types,
    get_flashcard_fsrs
)
from ..services.flashcards import review_card

router = APIRouter(
    prefix="/flashcards",
    tags=['flashcards'],
    responses={404: {"description": "Not found"}}
)

@router.post("/create")
def create_flashcard_endpoint(
    user: Annotated[UserIdentity, Depends(get_active_user)],
    db: Annotated[Session, Depends(get_db)],
    flashcards: list[FlashcardCreate]
):
    user_id = user.user_id
    for flashcard in flashcards:
        create_flashcard(db, user_id, flashcard)

@router.get("/find", response_model=list[int])
def find_flashcard_by_id_endpoint(
    user: Annotated[UserIdentity, Depends(get_active_user)],
    db: Annotated[Session, Depends(get_db)],
    language_id: Annotated[int | None, Query()] = None,
    flashcard_type: Annotated[int | None, Query()] = None
):
    user_id = user.user_id
    flashcards_id = get_all_flashcards_by_user_id(db, user_id, language_id, flashcard_type)
    
    return [flashcard_id.flashcard_id for flashcard_id in flashcards_id]

@router.get("/info")
def get_flashcard_info():
    pass

@router.put("/update")
def update_flashcard_endpoint():
    pass
    
@router.delete("/delete")
def delete_flashcard():
    pass

@router.patch('/review')
def review_flashcard_endpoint(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], flashcard_id: int, rating: RatingEnum):
    user_id = user.user_id
    flashcard_fsrs = get_flashcard_fsrs(db, flashcard_id, user_id)

    if flashcard_fsrs:
        updated_flashcard = review_card(flashcard_fsrs, rating)
    
    return updated_flashcard

@router.get('/types', response_model=list[FlashcardTypes])
def get_flashcard_types_endpoint(db: Annotated[Session, Depends(get_db)]):
    flashcard_types = get_flashcards_types(db)
    return flashcard_types