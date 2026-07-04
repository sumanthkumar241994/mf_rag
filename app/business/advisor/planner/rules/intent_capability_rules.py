from app.business.advisor.enums.capabilities import Capability
from app.business.advisor.enums.intent import Intent


INTENT_CAPABILITY_RULES: dict[Intent, set[Capability]] = {

    # ------------------------------------------------------------------
    # Conversation
    # ------------------------------------------------------------------

    Intent.GREETING: {
        Capability.GENERAL_ADVISOR,
    },

    Intent.CHITCHAT: {
        Capability.GENERAL_ADVISOR,
    },

    Intent.HELP: {
        Capability.GENERAL_ADVISOR,
    },

    # ------------------------------------------------------------------
    # Advice / Planning
    # ------------------------------------------------------------------

    Intent.RECOMMENDATION: {
        Capability.GENERAL_ADVISOR,
    },

    # ------------------------------------------------------------------
    # Unknown
    # ------------------------------------------------------------------

    Intent.UNKNOWN: {
        Capability.GENERAL_ADVISOR,
    },
}