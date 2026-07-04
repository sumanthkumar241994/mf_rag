from app.business.advisor.enums.intent import Intent
from app.business.advisor.enums.intent_priority import INTENT_PRIORITY
from app.business.advisor.planner.rules.intent_rules import INTENT_RULES


class IntentClassifier:
    def classify(self, query: str) -> Intent:
        query = query.lower().strip()

        matched: list[Intent] = []

        for intent, keywords in INTENT_RULES.items():
            if any(keyword in query for keyword in keywords):
                matched.append(intent)

        if not matched:
            return Intent.UNKNOWN.value
        
        #return min(matched, key=lambda intent: INTENT_PRIORITY[intent])
        matched.sort(key=lambda intent: INTENT_PRIORITY[intent])
        primary_intent = matched[0]

        return primary_intent
