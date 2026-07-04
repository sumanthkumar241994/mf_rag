from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    base_delay_seconds: float = 0.5
    exponential_backoff: bool = True