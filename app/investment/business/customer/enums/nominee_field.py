from enum import StrEnum


class NomineeField(StrEnum):
    NAME = "name"
    RELATIONSHIP = "relationship"
    DATE_OF_BIRTH = "date_of_birth"
    GUARDIAN = "guardian"
    IDENTITY_TYPE = "identity_type"
    IDENTITY_NUMBER = "identity_number"
    EMAIL = "email"
    MOBILE = "mobile"