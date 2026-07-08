from app.business.advisor.enums.intent import Intent


INTENT_RULES: dict[Intent, list[str]] = {

    Intent.GREETING: [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
    ],

    Intent.CHITCHAT: [
        "how are you",
        "thank you",
        "thanks",
        "awesome",
        "good job",
        "nice",
    ],

    Intent.HELP: [
        "help",
        "support",
        "guide",
        "assist",
        "how do i",
        "how to",
    ],

    Intent.INFORMATION: [
        "what",
        "why",
        "when",
        "where",
        "who",
        "which",
        "tell me",
        "explain",
        "define",
    ],

    Intent.ANALYSIS: [
        "analyse",
        "analyze",
        "analysis",
        "review",
        "evaluate",
        "performance",
        "risk",
        "health",
        "portfolio review",
    ],

    Intent.COMPARISON: [
        "compare",
        "comparison",
        "difference",
        "better",
        "vs",
        "versus",
    ],

    Intent.RECOMMENDATION: [
        "recommend",
        "suggest",
        "should i",
        "top",
        "top fund",
        "top funds",
        "best fund",
        "which fund",
        "advise",
    ],

    Intent.PLANNING: [
        "plan",
        "planning",
        "goal",
        "retirement",
        "retire",
        "future",
        "child education",
        "wealth creation",
    ],

    Intent.EXECUTION: [
        "buy",
        "purchase",
        "redeem",
        "withdraw",
        "switch",
        "stp",
        "swp",
        "sip",
        "start sip",
        "stop sip",
    ],
}