from enum import StrEnum


class ParameterSource(StrEnum):
    QUERY = "query"
    CUSTOMER_PROFILE = "customer_profile"
    CUSTOMER_KNOWLEDGE = "customer_knowledge"
    PORTFOLIO = "portfolio"
    DEFAULT = "default"
    DERIVED = "derived"