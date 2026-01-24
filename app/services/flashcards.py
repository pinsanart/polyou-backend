from fsrs import Scheduler, Card, Rating, State

from ..schemas.flashcards import FlashcardReviewFSRS, StateEnum, RatingEnum

scheduler = Scheduler()

def map_rating(rating: RatingEnum) -> Rating:
    return {
        RatingEnum.AGAIN: Rating.Again,
        RatingEnum.HARD: Rating.Hard,
        RatingEnum.GOOD: Rating.Good
    }[rating]

FSRS_STATE_MAP = {
    StateEnum.LEARNING: State.Learning,
    StateEnum.REVIEW: State.Review,
    StateEnum.RELEARNING: State.Relearning,
}

REVERSE_STATE_MAP = {v: k for k, v in FSRS_STATE_MAP.items()}


def review_card(
    old_flashcard: FlashcardReviewFSRS,
    rating: RatingEnum,
) -> FlashcardReviewFSRS:

    card = Card(
        state=FSRS_STATE_MAP[old_flashcard.state],
        stability=old_flashcard.stability,
        difficulty=old_flashcard.difficulty,
        due=old_flashcard.due,
        last_review=old_flashcard.last_review,
    )

    fsrs_rating = map_rating(rating)

    updated_card, _ = scheduler.review_card(card, fsrs_rating)

    return FlashcardReviewFSRS(
        stability=updated_card.stability,
        difficulty=updated_card.difficulty,
        due=updated_card.due,
        last_review=updated_card.last_review,
        state=REVERSE_STATE_MAP[updated_card.state],
    )