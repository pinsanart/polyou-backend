class LanguageNotAvailableError(Exception):
    def __init__(self, message: str):
        self.message = message