from enum import Enum

class WorkflowType(str, Enum):
    ADVISOR = "advisor"

    INVESTMENT_PURCHASE = "investment_purchase"
    INVESTMENT_REDEMPTION = "investment_redemption"
    INVESTMENT_SWITCH = "investment_switch"
    INVESTMENT_STP = "investment_stp"
    INVESTMENT_SWP = "investment_swp"