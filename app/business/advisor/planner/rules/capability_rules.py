from app.business.advisor.enums.capabilities import Capability
from app.business.advisor.models.capability_rules import CapabilityRule


CAPABILITY_RULES: list[CapabilityRule] = [

    # ---------------------------------------------------------------------
    # Customer
    # ---------------------------------------------------------------------

    CapabilityRule(
        capability=Capability.CUSTOMER,
        keywords=["customer", "account", "investor"],
        synonyms=["my account", "customer account"],
        examples=[
            "Show my customer details",
            "What is my account status?"
        ],
        priority=10,
    ),

    CapabilityRule(
        capability=Capability.CUSTOMER_PROFILE,
        keywords=["profile"],
        synonyms=["investor profile", "my profile"],
        examples=[
            "Show my profile",
            "What is my investor profile?"
        ],
        priority=10,
    ),

    CapabilityRule(
        capability=Capability.CUSTOMER_PERSONA,
        keywords=["persona"],
        synonyms=["investor type", "risk personality"],
        examples=[
            "What kind of investor am I?"
        ],
    ),

    CapabilityRule(
        capability=Capability.ONBOARDING,
        keywords=["onboarding", "kyc", "registration"],
        synonyms=[
            "account opening",
            "verification",
            "kyc pending",
            "onboarding status",
        ],
        examples=[
            "Why is my onboarding pending?",
            "What is my KYC status?"
        ],
        priority=5,
    ),

    # ---------------------------------------------------------------------
    # Portfolio
    # ---------------------------------------------------------------------

    CapabilityRule(
        capability=Capability.PORTFOLIO,
        keywords=[
            "portfolio",
            "holdings",
            "allocation",
        ],
        synonyms=[
            "my investments",
            "investment summary",
            "portfolio review",
            "portfolio health",
        ],
        examples=[
            "Analyze my portfolio",
            "Review my holdings",
        ],
        priority=1,
        weight=1.0,
    ),

    # ---------------------------------------------------------------------
    # Investment
    # ---------------------------------------------------------------------

    CapabilityRule(
        capability=Capability.INVESTMENT,
        keywords=["invest", "investment"],
        synonyms=["start investing"],
    ),

    CapabilityRule(
        capability=Capability.SIP,
        keywords=["sip"],
        synonyms=["systematic investment plan"],
        examples=[
            "Start SIP",
            "Increase my SIP"
        ],
        priority=5,
    ),

    CapabilityRule(
        capability=Capability.LUMPSUM,
        keywords=["lumpsum"],
        synonyms=["lump sum"],
    ),

    CapabilityRule(
        capability=Capability.REDEMPTION,
        keywords=["redeem", "redemption"],
        synonyms=["withdraw", "sell investment"],
    ),

    CapabilityRule(
        capability=Capability.SWITCH,
        keywords=["switch"],
        synonyms=["switch fund"],
    ),

    CapabilityRule(
        capability=Capability.STP,
        keywords=["stp"],
        synonyms=["systematic transfer plan"],
    ),

    CapabilityRule(
        capability=Capability.SWP,
        keywords=["swp"],
        synonyms=["systematic withdrawal plan"],
    ),

    # ---------------------------------------------------------------------
    # Scheme
    # ---------------------------------------------------------------------

    CapabilityRule(
        capability=Capability.SCHEME,
        keywords=[
            "scheme",
            "fund",
            "mutual fund",
            "elss",
            "index fund",
            "etf",
            "balanced advantage",
            "contra",
            "small cap",
            "large cap",
            "mid cap",
            "flexi cap",
            "equity fund",
            "debt fund",
        ],
        synonyms=[
            "hybrid fund"
        ],
        examples=[
            "Tell me about HDFC Flexi Cap",
            "What is ELSS?"
        ],
        priority=3,
    ),

    CapabilityRule(
        capability=Capability.FUND_COMPARISON,
        keywords=[
            "compare",
            "comparison",
            "difference",
        ],
        synonyms=[
            "vs",
            "versus",
            "better fund",
        ],
        examples=[
            "Compare Parag Parikh and HDFC Flexi Cap"
        ],
        priority=2,
    ),

    CapabilityRule(
        capability=Capability.NAV,
        keywords=["nav"],
        synonyms=["net asset value"],
    ),

    # ---------------------------------------------------------------------
    # Goals
    # ---------------------------------------------------------------------

    CapabilityRule(
        capability=Capability.GOAL,
        keywords=["goal", "planning"],
        synonyms=["financial goal"],
        priority=5,
    ),

    CapabilityRule(
        capability=Capability.RETIREMENT,
        keywords=["retire", "retirement"],
        synonyms=["retire at", "pension"],
    ),

    CapabilityRule(
        capability=Capability.CHILD_EDUCATION,
        keywords=[
            "education",
            "college",
            "school",
        ],
        synonyms=[
            "child education",
        ],
    ),

    CapabilityRule(
        capability=Capability.WEALTH_CREATION,
        keywords=[
            "wealth",
            "wealth creation",
        ],
        synonyms=[
            "long term investment",
        ],
    ),

    # ---------------------------------------------------------------------
    # Risk
    # ---------------------------------------------------------------------

    CapabilityRule(
        capability=Capability.RISK_PROFILE,
        keywords=["risk profile"],
        synonyms=["risk appetite"],
    ),

    CapabilityRule(
        capability=Capability.RISK_ASSESSMENT,
        keywords=["risk"],
        synonyms=[
            "portfolio risk",
            "risk analysis",
        ],
    ),

    # ---------------------------------------------------------------------
    # Tax
    # ---------------------------------------------------------------------

    CapabilityRule(
        capability=Capability.TAX,
        keywords=["tax"],
        synonyms=["taxation", "income tax"],
    ),

    CapabilityRule(
        capability=Capability.CAPITAL_GAINS,
        keywords=["capital gain"],
        synonyms=[
            "ltcg",
            "stcg",
            "capital gains tax",
        ],
    ),

    # ---------------------------------------------------------------------
    # Transactions
    # ---------------------------------------------------------------------

    CapabilityRule(
        capability=Capability.TRANSACTION,
        keywords=["transaction"],
        synonyms=[
            "purchase",
            "payment",
            "order",
        ],
    ),

    # ---------------------------------------------------------------------
    # Documents
    # ---------------------------------------------------------------------

    CapabilityRule(
        capability=Capability.DOCUMENT,
        keywords=["document"],
        synonyms=[
            "pdf",
            "prospectus",
        ],
    ),

    CapabilityRule(
        capability=Capability.SID,
        keywords=["sid"],
        synonyms=["scheme information document"],
    ),

    CapabilityRule(
        capability=Capability.KIM,
        keywords=["kim"],
        synonyms=["key information memorandum"],
    ),

    CapabilityRule(
        capability=Capability.FACTSHEET,
        keywords=["factsheet"],
        synonyms=["fact sheet"],
    ),

    CapabilityRule(
        capability=Capability.ANNUAL_REPORT,
        keywords=["annual report"],
        synonyms=["report"],
    ),

    # ---------------------------------------------------------------------
    # Market
    # ---------------------------------------------------------------------

    CapabilityRule(
        capability=Capability.MARKET,
        keywords=["market"],
        synonyms=[
            "market outlook",
            "market update",
        ],
    ),

    CapabilityRule(
        capability=Capability.NEWS,
        keywords=["news"],
        synonyms=[
            "latest news",
            "market news",
        ],
    ),

    # ---------------------------------------------------------------------
    # Advisor
    # ---------------------------------------------------------------------

    CapabilityRule(
        capability=Capability.ADVISOR,
        keywords=[
            "recommend",
            "suggest",
            "advise",
            "help",
        ],
        synonyms=[
            "should i",
            "guide me",
        ],
        priority=100,
        weight=0.2,
    ),
]