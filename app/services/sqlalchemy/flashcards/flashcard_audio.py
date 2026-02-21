from typing import List

from ....core.services.flashcards.flashcard_audio import FlashcardAudioService
from ....core.schemas.flashcards.bases import FlashcardAudioBase
from ....core.schemas.flashcards.models import FlashcardAudio

from ....infrastructure.repository.sqlalchemy.flashcards.flashcard_audio import FlashcardAudioRepositorySQLAlchemy
from ....infrastructure.db.models import FlashcardAudioModel

class FlashcardAudioServiceSQLAlchemy(FlashcardAudioService):
    def __init__(self, flashcard_audio_repository: FlashcardAudioRepositorySQLAlchemy):
        self.flashcard_audio_repository = flashcard_audio_repository
    
    def info_all(self, flashcard_id: int) -> List[FlashcardAudio]:
        models = self.flashcard_audio_repository.get_all(flashcard_id)
        return [FlashcardAudio.model_validate(model) for model in models]
    
    def change(self, flashcard_id, new_audios: List[FlashcardAudioBase]) -> None:
        models = [
            FlashcardAudioModel(
                flashcard_id = flashcard_id,
                **audio.model_dump(exclude_unset=True)
            ) 
            for audio in new_audios
        ]
        self.flashcard_audio_repository.delete_all_for_id(flashcard_id)
        self.flashcard_audio_repository.create_many(models)