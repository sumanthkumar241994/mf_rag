from enum import StrEnum


class ComplianceFindingType(StrEnum):
    POLICY = "POLICY"
    PII = "PII"
    DISCLAIMER = "DISCLAIMER"
    CITATION = "CITATION"