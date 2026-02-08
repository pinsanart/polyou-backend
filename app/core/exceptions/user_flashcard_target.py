class TargetLanguageAlreadyExistsError(Exception):
    def __init__(self, message: str):
        self.message = message

class NotAddedTargetLanguage(Exception):
    def __init__(self, message: str):
        self.message = message