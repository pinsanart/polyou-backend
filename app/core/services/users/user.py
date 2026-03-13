from abc import ABC, abstractmethod

class UserService(ABC):
    @abstractmethod
    def get_public_id_or_fail(self, user_id):
        pass

    @abstractmethod
    def register(self, register_information):
        pass