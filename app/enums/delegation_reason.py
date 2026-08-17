from enum import StrEnum


class DelegationReason(StrEnum):
    SCHEME_SELECTION = "scheme_selection"
    SCHEME_DETAILS = "scheme_details"
    ADVISORY_REQUIRED = "advisory_required"
    EXECUTION_REQUEST = "execution_request"