from enum import StrEnum


class RequirementStatus(StrEnum):
    REQUIRED = "required"
    PENDING = "pending"
    COMPLETED = "completed"