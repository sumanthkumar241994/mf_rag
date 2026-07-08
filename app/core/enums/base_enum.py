from enum import StrEnum


class BaseEnum(StrEnum):

    @classmethod
    def from_value(cls, value: str | None):
        if value is None:
            return cls.UNKNOWN
        
        try:
            return cls(value)
        except ValueError:
            return cls.UNKNOWN
        
    @property
    def display_name(self) -> str:
        return self.name.replace("_", " ").title()
