class JWTTokenMissingSubjectError(Exception):
    def __init__(self, message: str):
        self.message = message

class JWTTokenExpiredSignatureError(Exception):
    def __init__(self, message: str):
        self.message = message

class JWTInvalidTokenError(Exception):
    def __init__(self, message: str):
        self.message = message
