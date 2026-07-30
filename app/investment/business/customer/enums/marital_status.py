from app.core.enums.base_enum import BaseEnum


class MaritalStatus(BaseEnum):
    MARRIED = '01'
    UNMARRIED ='02'
    UNKNOWN = "UNKKNOWN"

    @property
    def display_name(self) -> str:
        return {
            self.MARRIED : "married",
            self.UNMARRIED: "unmarried",
            self.UNKNOWN: "unknown/other"
        }[self]