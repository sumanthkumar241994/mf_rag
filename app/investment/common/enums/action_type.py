from enum import StrEnum


class ActionType(StrEnum):
    CONTACT_SUPPORT = 'contact_support'
    REQUEST_DATA_COLLECTION = 'request_data_collection'
    CHECK_ELIGIBILITY = 'check_eligibility'
    CHECK_CUSTOMER = "check_customer"
    REFRESH_CUSTOMER = 'refresh_customer'
    CHECK_NOMINEE = "check_nominee"
    UPDATE_NOMINEE = "update_nominee"
    UPDATE_SIGNATURE = "update_signature"

    CHECK_KYC = "check_kyc"
    COMPLETE_KYC = "complete_kyc"

    CHECK_BANK = "check_bank"
    UPDATE_BANK = "update_bank"
    UPDATE_FATCA = "update_fatca"

    RESOLVE_SCHEME = "resolve_scheme"

    DELEGATE_ADVISOR = "delegate_advisor"

    CREATE_INVESTMENT = "create_investment"

    REQUEST_OTP = "request_otp"

    POLL_STATUS = "poll_status"

    COMPLETE = "complete"