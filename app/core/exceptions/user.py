class UserError(Exception):
    def __init__(self):
        self.message = "USER ERROR: "

class EmailAlreadyExistsError(UserError):
    def __init__(self, message):
        self.message += message 