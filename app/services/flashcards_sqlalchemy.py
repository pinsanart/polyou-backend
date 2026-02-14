from ..core.services.flashcards import FlashcardService
from ..core.schemas.flashcards import (
    FlashcardCreateInfo, 
    FlashcardInfo,
    FlashcardContent,
    FlashcardFSRS,
    FlashcardReview,
    FlashcardAudio,
    FlashcardImage,
    FlashcardMetadata,
    FlashcardMetadataResponse
)
from ..infrastructure.repository.flashcards_sqlalchemy import FlashcardRepositorySQLAlchemy
from .user_target_language import UserTargetLanguageServiceSQLAlchemy
from .flascards_types_sqlalchemy import FlashcardsTypesServiceSQLAlchemy
from ..core.exceptions.flashcards import PublicIDDoesNotBelongToUserError
from ..services.languages_sqlalchemy import LanguageServiceSQLAlchemy
from ..infrastructure.db.models import (
    FlashcardContentModel, 
    FlashcardImagesModel, 
    FlashcardAudiosModel, 
    FlashcardFSRSModel, 
    FlashcardModel,
    FlashcardReviewModel,
    FlashcardMetadataModel
)
from uuid import UUID

class FlashcardServiceSQLAlchemy(FlashcardService):
    def __init__(self, flashcards_repository: FlashcardRepositorySQLAlchemy, user_target_language_service: UserTargetLanguageServiceSQLAlchemy, flashcard_type_service: FlashcardsTypesServiceSQLAlchemy, language_service: LanguageServiceSQLAlchemy):
        super().__init__(flashcards_repository, user_target_language_service, flashcard_type_service, language_service)

    def _to_flashcard_model(self, user_id: int, flashcard_info: FlashcardCreateInfo) -> FlashcardModel:
        language_iso_639_1 = flashcard_info.language_iso_639_1
        flashcard_type_name = flashcard_info.flashcard_type_name

        public_id = flashcard_info.public_id
        language_id = self.user_target_language_service.get_user_language_id_by_iso_639_1(user_id, language_iso_639_1)
        flashcard_type_id = self.flashcard_types_service.get_id_by_name_or_fail(flashcard_type_name)

        if flashcard_info.metadata:
            metadata = FlashcardMetadataModel(
                created_at = flashcard_info.metadata.created_at,
                last_review_at = flashcard_info.metadata.last_review_at,
                last_content_updated_at = flashcard_info.metadata.last_content_updated_at
            )
        else:
            metadata = FlashcardMetadataModel()

        fsrs = FlashcardFSRSModel(
            stability = flashcard_info.fsrs.stability, 
            difficulty = flashcard_info.fsrs.difficulty,
            due = flashcard_info.fsrs.due,
            last_review = flashcard_info.fsrs.last_review,
            state = flashcard_info.fsrs.state
        )

        content = FlashcardContentModel(
            front_field_content = flashcard_info.content.front_field, 
            back_field_content = flashcard_info.content.front_field
        )

        images = [
            FlashcardImagesModel(
                field = flashcard_image.field,
                image_url= flashcard_image.image_url
            )
            for flashcard_image in flashcard_info.images
        ]

        audios = [
            FlashcardAudiosModel(
                field = flashcard_audio.field,
                audio_url = flashcard_audio.audio_url
            )
            for flashcard_audio in flashcard_info.audios
        ]
        
        reviews = [
            FlashcardReviewModel (
                reviewed_at = review.reviewed_at,
                rating = review.rating,
                response_time_ms = review.response_time_ms,
                scheduled_days = review.scheduled_days,
                actual_days = review.actual_days,
                prev_stability = review.prev_stability,
                prev_difficulty = review.prev_difficulty,
                new_stability = review.new_stability,
                new_difficulty = review.new_difficulty,
                state_before = review.state_before,
                state_after = review.state_after
            )

            for review in flashcard_info.reviews
        ]

        model = FlashcardModel(
            public_id = public_id,
            user_id = user_id,
            language_id = language_id,
            flashcard_type_id = flashcard_type_id,

            server_metadata = metadata,
            content = content,
            fsrs = fsrs,
            reviews = reviews,
            images = images,
            audios=audios,
        )

        return model

    def _to_flashcard_info(self, flashcard_model: FlashcardModel) -> FlashcardInfo:
        language_iso_639_1 = self.language_service.get_iso_639_1_by_id(flashcard_model.language_id)
        flashcard_type_name = self.flashcard_types_service.get_name_by_id(flashcard_model.flashcard_type_id)

        content = FlashcardContent(
            front_field= flashcard_model.content.front_field_content,
            back_field= flashcard_model.content.back_field_content
        )

        fsrs  = FlashcardFSRS(
            stability= flashcard_model.fsrs.stability,
            difficulty=flashcard_model.fsrs.difficulty,
            due= flashcard_model.fsrs.due,
            last_review= flashcard_model.fsrs.last_review,
            state= flashcard_model.fsrs.state
        )

        reviews = [
            FlashcardReview(
                reviewed_at = review.reviewed_at,
                rating = review.rating,
                response_time_ms = review.response_time_ms,
                
                scheduled_days = review.scheduled_days,
                actual_days = review.actual_days,

                prev_stability = review.prev_stability,
                prev_difficulty = review.prev_difficulty,
                new_stability = review.new_stability,
                new_difficulty = review.new_difficulty,

                state_before = review.state_before,
                state_after = review.state_after
            )
            for review in flashcard_model.reviews
        ]

        audios = [
            FlashcardAudio(
                field = audio.field,
                audio_url = audio.audio_url
            )
            for audio in flashcard_model.audios
        ]

        images = [
            FlashcardImage(
                field= image.field,
                image_url = image.image_url
            )
            for image in flashcard_model.images
        ]

        matadata = FlashcardMetadata(
            created_at= flashcard_model.server_metadata.created_at,
            last_review_at= flashcard_model.server_metadata.last_review_at,
            last_content_updated_at= flashcard_model.server_metadata.last_content_updated_at
        )

        flashcard_info = FlashcardInfo(
            public_id = flashcard_model.public_id,
            language_iso_639_1 = language_iso_639_1,
            flashcard_type_name = flashcard_type_name,
            metadata = matadata,
            content = content,
            fsrs= fsrs,
            reviews= reviews,
            audios= audios,
            images= images
        )

        return flashcard_info

    def create_one(self, user_id: int, flashcard_info:FlashcardCreateInfo):
        flashcard_model = self._to_flashcard_model(user_id, flashcard_info)
        self.flashcards_repository.create(flashcard_model)
        return flashcard_model.public_id

    def create_many(self, user_id: int, flashcards_info: list[FlashcardCreateInfo]):
        models = []
        for flashcard_info in flashcards_info:
            model = self._to_flashcard_model(user_id, flashcard_info)
            models.append(model)
        
        public_ids = []
        for model in models:
            self.flashcards_repository.create(model)
            public_ids.append(model.public_id)
        
        return public_ids

    def list_public_ids(self, user_id: int):
        flashcards_ids = self.flashcards_repository.list_ids(user_id)
        
        public_ids = []
        for flashcard_id in flashcards_ids:
            model = self.flashcards_repository.get_by_id(flashcard_id)
            public_ids.append(model.public_id)
        
        return public_ids

    def _get_flashcard_id_by_public_id_or_fail(self, public_id: UUID, user_id:int):
        user_public_ids = self.list_public_ids(user_id)

        if public_id not in user_public_ids:
                raise PublicIDDoesNotBelongToUserError(f"The public id '{public_id}' does not belong the the authenticated user.")
        
        flashcard =  self.flashcards_repository.get_by_public_id(public_id)

        return flashcard.flashcard_id

    def delete_one(self, user_id, public_id: UUID):
        flashcard_id = self._get_flashcard_id_by_public_id_or_fail(public_id, user_id)
        self.flashcards_repository.delete(flashcard_id)

    def delete_many(self, user_id, public_ids:list[UUID]):
        flashcards_ids = []
        for public_id in public_ids:
            flashcard_id = self._get_flashcard_id_by_public_id_or_fail(public_id, user_id)
            flashcards_ids.append(flashcard_id)
        
        for flashcard_id in flashcards_ids:
            self.flashcards_repository.delete(flashcard_id)
        
    def info(self, user_id, public_ids:list) -> list[FlashcardInfo]:
        flashcards_ids = []
        for public_id in public_ids:
            flashcard_id = self._get_flashcard_id_by_public_id_or_fail(public_id, user_id)
            flashcards_ids.append(flashcard_id)

        flashcards_info = []
        for flashcard_id in flashcards_ids:
            flashcard_model = self.flashcards_repository.get_by_id(flashcard_id)
            flashcard_info = self._to_flashcard_info(flashcard_model)
            flashcards_info.append(flashcard_info)

        return flashcards_info
    
    def metadata(self, user_id: int, public_id: UUID) -> FlashcardMetadataResponse:
        flashcard_id = self._get_flashcard_id_by_public_id_or_fail(public_id, user_id)
        flashcard_model = self.flashcards_repository.get_by_id(flashcard_id)
        
        return FlashcardMetadataResponse(
            public_id = flashcard_model.public_id,
            created_at= flashcard_model.server_metadata.created_at,
            last_review_at= flashcard_model.server_metadata.last_review_at,
            last_content_updated_at= flashcard_model.server_metadata.last_content_updated_at
        )
    
        
    
    def all_metadata(self, user_id: int) -> list[FlashcardMetadataResponse]:
        flashcards_ids = self.flashcards_repository.list_ids(user_id)
        
        metadatas = []
        for id in flashcards_ids:
            flashcard_model = self.flashcards_repository.get_by_id(id)
            metadata = FlashcardMetadataResponse(
                public_id = flashcard_model.public_id,
                created_at= flashcard_model.server_metadata.created_at,
                last_review_at= flashcard_model.server_metadata.last_review_at,
                last_content_updated_at= flashcard_model.server_metadata.last_content_updated_at
            )
            metadatas.append(metadata)

        return metadatas