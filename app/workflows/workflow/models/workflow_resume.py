from dataclasses import dataclass


@dataclass(slots=True)
class WorkflowResume:
    answer: str