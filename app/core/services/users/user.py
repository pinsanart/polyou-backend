from abc import ABC, abstractmethod

class UserService(ABC):
    @abstractmethod
    def register(self, register_information):
        pass