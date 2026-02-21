from abc import ABC, abstractmethod

class FlashcardAudioRepository(ABC):
    @abstractmethod
    def get_all(self, flashcard_id):
        pass

    @abstractmethod
    def delete_all_for_id(self, flashcard_id):
        pass

    @abstractmethod
    def create_one(self, audio_model):
        pass

    @abstractmethod
    def create_many(self, audios_models):
        pass