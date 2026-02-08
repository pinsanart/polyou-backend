class AuthError(Exception):
    def __init__(self):
        self.message = "AUTH ERROR: "

class InvalidCredentials(AuthError):
    def __init__(self, message: str):
        super().__init__()
        self.message += message

class UserDisabled(AuthError):
    def __init__(self, message: str):
        super().__init__()
        self.message += message

class UserNotFound(AuthError):
    def __init__(self, message: str):
        super().__init__()
        self.message += message
