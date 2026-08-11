from enum import StrEnum


class AddressType(StrEnum):
    RESIDENCE = "01"
    BUSINESS = "02"
    RESIDENCE_AND_BUSINESS = "03"

    @classmethod
    def from_api(cls, value: str | None) -> "AddressType | None":
        if value is None:
            return None

        try:
            # API returned "01"
            return cls(value)
        except ValueError:
            # API returned "RESIDENCE"
            return cls[value]