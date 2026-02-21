from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from .....core.repositories.flashcards.flashcard_audio import FlashcardAudioRepository
from ....db.models import FlashcardAudioModel

class FlashcardAudioRepositorySQLAlchemy(FlashcardAudioRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all(self, flashcard_id: int) -> List[FlashcardAudioModel]:
        stmt = select(FlashcardAudioModel).where(FlashcardAudioModel.flashcard_id == flashcard_id)
        return self.db_session.scalars(stmt).all()

    def delete_all_for_id(self, flashcard_id: int) -> None:
        stmt = select(FlashcardAudioModel).where(FlashcardAudioModel.flashcard_id == flashcard_id)
        audios_models = self.db_session.scalars(stmt).all()
        for audio_model in audios_models:
            self.db_session.delete(audio_model)

    def create_one(self, audio_model: FlashcardAudioModel) -> None:
        self.db_session.add(audio_model)
    
    def create_many(self, audios_models: List[FlashcardAudioModel]):
        self.db_session.add_all(audios_models)