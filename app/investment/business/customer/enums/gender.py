from enum import StrEnum

from app.core.enums.base_enum import BaseEnum


class Gender(BaseEnum):
    MALE = "M"
    FEMALE = 'F'
    OTHER = 'O'
    UNKNOWN = 'UNKNOWN'

    @property
    def display_name(self) -> str:
        return {
            self.MALE: "Male",
            self.FEMALE: "Female",
            self.OTHER: "Other",
            self.UNKNOWN: "Unknown",
        }[self]