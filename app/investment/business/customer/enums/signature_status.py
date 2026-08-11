from app.core.enums.base_enum import BaseEnum


class SignatureStatus(BaseEnum):
    NOT_UPLOADED = "not_uploaded"
    UPLOADED = "uploaded"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    UNKNOWN = "unknown"

    @property
    def display_name(self) -> str:
        ...

    @property
    def description(self) -> str:
        ...

    @property
    def requires_customer_action(self) -> bool:
        return self in (
            self.NOT_UPLOADED,
            self.REJECTED,
        )

    @property
    def is_pending(self) -> bool:
        return self is self.UPLOADED

    @property
    def is_completed(self) -> bool:
        return self is self.ACCEPTED