from app.core.enums.base_enum import BaseEnum


class OnboardingStatus(BaseEnum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    PROCESSING = "PROCESSING"
    UNKNOWN = "UNKNOWN"

    @property
    def display_name(self) -> str:
        ...

    @property
    def description(self) -> str:
        ...

    @property
    def is_completed(self) -> bool:
        return self is self.SUCCESS

    @property
    def is_pending(self) -> bool:
        return self is self.PROCESSING