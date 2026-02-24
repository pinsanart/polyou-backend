class PublicIDDoesNotBelongToUserError(Exception):
    def __init__(self, message: str):
        self.message = message

class PublicIDAlreadyRegistedError(Exception):
    def __init__(self, message: str):
        self.message = message

class PublicIDDoesNotExistError(Exception):
    def __init__(self, message: str):
        self.message = message
    
class FlashcardTypeNameNotExistError(Exception):
    def __init__(self, message: str):
        self.message = message
    