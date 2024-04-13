from enum import Enum


class ResultStatus(str, Enum):
    REJECTED = "REJECTED"
    ACCEPTED = "ACCEPTED"
