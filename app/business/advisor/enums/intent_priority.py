from app.business.advisor.enums.intent import Intent

INTENT_PRIORITY: dict[Intent, int] = {
    Intent.EXECUTION: 1,
    Intent.RECOMMENDATION: 2,
    Intent.PLANNING: 3,
    Intent.COMPARISON: 4,
    Intent.ANALYSIS: 5,
    Intent.INFORMATION: 6,
    Intent.HELP: 7,
    Intent.CHITCHAT: 8,
    Intent.GREETING: 9,
    Intent.UNKNOWN: 10,
}