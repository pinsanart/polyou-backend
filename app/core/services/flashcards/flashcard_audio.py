from abc import ABC, abstractmethod

class FlashcardAudioService(ABC):
    @abstractmethod
    def info_all(self, flashcard_id):
        pass

    @abstractmethod
    def change(self, flashcard_id, new_audios):
        pass