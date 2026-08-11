from enum import StrEnum


class ConversationWorkflow(StrEnum):
    ADVISOR = "advisor"
    INVESTMENT_LUMPSUM = "investment_lumpsum"
    INVESTMENT_SIP = "investment_sip"
    INVESTMENT_REDEMPTION = "investment_redemption"
    INVESTMENT_SWITCH = "investment_switch"
    INVESTMENT_STP = "investment_stp"
    INVESTMENT_SWP = "investment_swp"