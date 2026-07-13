from enum import StrEnum


class Capability(StrEnum):
    """
    Business capabilities supported by the Advisor Platform.

    A single user request may require multiple capabilities.
    """
    # Customer
    CUSTOMER = "customer"
    CUSTOMER_PROFILE = "customer_profile"
    CUSTOMER_PERSONA = "customer_persona"
    ONBOARDING = "onboarding"
    KYC = "kyc"
    NOMINEE = "nominee"

    # Portfolio
    PORTFOLIO = "portfolio"
    PORTFOLIO_PERFORMANCE = "portfolio_performance"
    PORTFOLIO_RISK = "portfolio_risk"
    PORTFOLIO_DIVERSIFICATION = "portfolio_diversification"
    PORTFOLIO_HEALTH = "portfolio_health"

    # Investment
    INVESTMENT = "investment"
    SIP = "sip"
    LUMPSUM = "lumpsum"
    REDEMPTION = "redemption"
    SWITCH = "switch"
    STP = "stp"
    SWP = "swp"

    # Goal Planning
    GOAL = "goal"
    RETIREMENT = "retirement"
    CHILD_EDUCATION = "education"
    WEALTH_CREATION = "wealth_creation"
    EMERGENCY_FUND = "emergency_fund"

    # Scheme / Fund
    SCHEME = "scheme"
    SCHEME_DETAILS = "scheme_details"
    FUND_COMPARISON = "fund_comparison"
    NAV = "nav"

    # Risk
    RISK_PROFILE = "risk_profile"
    RISK_ASSESSMENT = "risk_assessment"

    # Tax
    TAX = "tax"
    CAPITAL_GAINS = "capital_gains"
    TAX_SAVING = "tax_saving"

    # Transactions
    TRANSACTION = "transaction"
    TRANSACTION_HISTORY = "transaction_history"

    # Documents (RAG)
    DOCUMENT = "document"
    SID = "sid"
    KIM = "kim"
    FACTSHEET = "factsheet"
    ANNUAL_REPORT = "annual_report"
    FUND_MANAGER_COMMENTARY = "fund_manager_commentary"
    MARKET_OUTLOOK = "market_outlook"

    # Market
    MARKET = "market"
    NEWS = "news"

    # General Advisor
    ADVISOR = "advisor"