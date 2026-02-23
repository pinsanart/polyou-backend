class InvalidCredentials(Exception):
    def __init__(self, message: str):
        self.message = message

class UserDisabled(Exception):
    def __init__(self, message: str):
        self.message = message

class UserNotFound(Exception):
    def __init__(self, message: str):
        self.message = message

class RefreshTokenNotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message

class RefreshTokenRevokedError(Exception):
    def __init__(self, message: str):
        self.message = message

class RefreshTokenExpiredError(Exception):
    def __init__(self, message: str):
        self.message = message