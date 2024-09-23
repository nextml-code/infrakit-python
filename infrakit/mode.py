from enum import Enum


class Mode(str, Enum):
    PRODUCTION = "production"
    BETA = "beta"
    TEST = "test"
