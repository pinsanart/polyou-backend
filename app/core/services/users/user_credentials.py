from abc import ABC, abstractmethod

class UserCredentialsService(ABC):
    @abstractmethod
    def info(self, user_id):
        pass

    @abstractmethod
    def change(self, user_id, new_credentials):
        pass