from abc import ABC, abstractmethod

class UserMetadataRepository(ABC):
    @abstractmethod
    def get(self, user_id):
        pass

    @abstractmethod
    def update(self, user_id, data):
        pass