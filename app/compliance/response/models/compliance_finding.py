from dataclasses import dataclass

from app.compliance.enums.severity import Severity



@dataclass(frozen=True)
class ComplianceFinding:
    """
    Represents a compliance issue detected during validation.
    """

    type: str
    description: str
    severity: Severity