from enum import StrEnum

from app.core.enums.base_enum import BaseEnum


class NomineeIdentityType(BaseEnum):
    PAN = "1"
    AADHAAR = "2"
    DRIVING_LICENSE = "3"
    PASSPORT = "4"
    UNKNOWN = "UNKNOWN"

    @property
    def display_name(self) -> str:
        return {
            self.PAN: "PAN",
            self.AADHAAR: "Aadhaar",
            self.DRIVING_LICENSE: "Driving License",
            self.PASSPORT: "Passport",
            self.UNKNOWN: "Unknown",
        }[self]