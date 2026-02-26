from enum import Enum

class Fields(str, Enum):
    front = "front"
    back = "back"

class FSRSState(int, Enum):
    LEARNING = 1
    REVIEW = 2
    RELEARNING = 3

class FSRSRating(int, Enum):
    AGAIN = 1
    HARD = 2
    GOOD = 3