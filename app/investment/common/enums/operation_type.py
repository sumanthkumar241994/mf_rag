from enum import StrEnum


class OperationType(StrEnum):
    INVEST = "invest"
    REDEEM = "redeem"
    SWITCH = "switch"
    START_SIP = "start_sip"
    STOP_SIP = "stop_sip"
    UPDATE_NOMINEE = "update_nominee"
    UPDATE_FATCA = 'update_fatca'
    UPDATE_BANK = "update_bank"
    COMPLETE_KYC = "complete_kyc"