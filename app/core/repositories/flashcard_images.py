from abc import ABC, abstractmethod

class FlashcardImagesRepository(ABC):
    @abstractmethod
    def delete_all_for_id(self, flashcard_id):
        pass

    @abstractmethod
    def create_one(self, flashcard_id, image):
        pass

    @abstractmethod
    def create_many(self, flashcard_id, images:list):
        pass

