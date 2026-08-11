from enum import StrEnum


class CustomerState(StrEnum):
    NOT_LOADED = "not_loaded"
    STALE = "stale"
    FRESH = "fresh"