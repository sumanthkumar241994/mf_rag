from app.business.advisor.enums.capabilities import Capability
from app.business.advisor.enums.tool_type import ToolType


CAPABILITY_TOOL_RULES: dict[Capability, list[ToolType]] = {

    # ------------------------------------------------------------------
    # Customer
    # ------------------------------------------------------------------

    Capability.CUSTOMER: [
        ToolType.CUSTOMER,
    ],

    Capability.CUSTOMER_PROFILE: [
        ToolType.CUSTOMER,
    ],

    Capability.CUSTOMER_PERSONA: [
        ToolType.CUSTOMER,
    ],

    Capability.ONBOARDING: [
        ToolType.CUSTOMER,
    ],

    # ------------------------------------------------------------------
    # Portfolio
    # ------------------------------------------------------------------

    Capability.PORTFOLIO: [
        ToolType.PORTFOLIO,
    ],

    # ------------------------------------------------------------------
    # Investments
    # ------------------------------------------------------------------

    Capability.INVESTMENT: [
        ToolType.INVESTMENT,
    ],

    Capability.SIP: [
        ToolType.INVESTMENT,
    ],

    Capability.LUMPSUM: [
        ToolType.INVESTMENT,
    ],

    Capability.REDEMPTION: [
        ToolType.INVESTMENT,
    ],

    Capability.SWITCH: [
        ToolType.INVESTMENT,
    ],

    Capability.STP: [
        ToolType.INVESTMENT,
    ],

    Capability.SWP: [
        ToolType.INVESTMENT,
    ],

    # ------------------------------------------------------------------
    # Goal Planning
    # ------------------------------------------------------------------

    Capability.GOAL: [
        ToolType.GOAL,
    ],

    Capability.RETIREMENT: [
        ToolType.GOAL,
    ],

    Capability.CHILD_EDUCATION: [
        ToolType.GOAL,
    ],

    Capability.WEALTH_CREATION: [
        ToolType.GOAL,
    ],

    # ------------------------------------------------------------------
    # Risk
    # ------------------------------------------------------------------

    Capability.RISK_PROFILE: [
        ToolType.RISK,
    ],

    Capability.RISK_ASSESSMENT: [
        ToolType.RISK,
    ],

    # ------------------------------------------------------------------
    # Documents / Knowledge Base
    # ------------------------------------------------------------------

    Capability.DOCUMENT: [
        ToolType.DOCUMENT_SEARCH,
    ],

    Capability.SCHEME: [
        ToolType.SCHEME,
    ],

    Capability.FUND_COMPARISON: [
        ToolType.SCHEME,
    ],

    Capability.NAV: [
        ToolType.SCHEME,
    ],

    Capability.SID: [
        ToolType.DOCUMENT_SEARCH,
    ],

    Capability.KIM: [
        ToolType.DOCUMENT_SEARCH,
    ],

    Capability.FACTSHEET: [
        ToolType.DOCUMENT_SEARCH,
    ],

    Capability.ANNUAL_REPORT: [
        ToolType.DOCUMENT_SEARCH,
    ],

    # ------------------------------------------------------------------
    # Market
    # ------------------------------------------------------------------

    Capability.MARKET: [
        ToolType.MARKET,
    ],

    Capability.NEWS: [
        ToolType.MARKET,
    ],

    # ------------------------------------------------------------------
    # Tax
    # ------------------------------------------------------------------

    Capability.TAX: [
        ToolType.ADVISOR,
    ],

    Capability.CAPITAL_GAINS: [
        ToolType.ADVISOR,
    ],

    # ------------------------------------------------------------------
    # Transactions
    # ------------------------------------------------------------------

    Capability.TRANSACTION: [
        ToolType.INVESTMENT,
    ],

    # ------------------------------------------------------------------
    # General Advisor
    # ------------------------------------------------------------------

    Capability.ADVISOR: [
        ToolType.ADVISOR,
    ],
}