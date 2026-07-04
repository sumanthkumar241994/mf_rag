from enum import StrEnum


class ApprovalPolicy(StrEnum):
    AUTO ='auto'
    OPTIONAL ='optional'
    REQUIRED ='required'