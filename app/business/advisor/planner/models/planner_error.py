from dataclasses import dataclass


@dataclass
class PlannerError:
    field: str
    message: str