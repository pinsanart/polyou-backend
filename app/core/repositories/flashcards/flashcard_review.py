from abc import ABC, abstractmethod

class FlashcardReviewRepository(ABC):
    @abstractmethod
    def get_all(self, flashcard_id):
        pass

    @abstractmethod
    def delete_all_for_id(self, flashcard_id):
        pass

    @abstractmethod
    def create_one(self, review_model):
        pass

    @abstractmethod
    def create_many(self, review_models):
        pass