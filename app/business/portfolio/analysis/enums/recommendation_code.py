from enum import StrEnum

class RecommendationCode(StrEnum):
    DIVERSIFY_PORTFOLIO = "diversify_portfolio"
    REVIEW_UNDERPERFORMING_FUNDS = "review_underperforming_funds"
    REDUCE_PORTFOLIO_RISK = "reduce_portfolio_risk"
    REDUCE_CONCENTRATION = "reduce_concentration"
    MAINTAIN_PORTFOLIO = "maintain_portfolio"
    CONTINUE_CURRENT_SIP = "continue_current_sip"
    INCREASE_SIP = "increase_sip"
    REVIEW_GOAL = "review_goal"