from abc import abstractmethod

from ..service import Service

class UserService(Service):
    @abstractmethod
    def register(self, register_information):
        pass