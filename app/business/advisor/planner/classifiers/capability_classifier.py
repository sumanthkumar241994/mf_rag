from app.business.advisor.enums.capabilities import Capability
from app.business.advisor.enums.intent import Intent
from app.business.advisor.models.capability_match import CapabilityMatch
from app.business.advisor.planner.rules.capability_rules import CAPABILITY_RULES


class CapabilityClassifier:
    def classify(self, query: str, intent: Intent) -> list[Capability]:
        query =query.lower().strip()

        matches : dict[Capability, CapabilityMatch] = {}

        # Higher priority rules evaluated first
        rules = sorted(CAPABILITY_RULES, key=lambda rule:rule.priority)

        for rule in rules:
            phrases = [
                *rule.keywords,
                *rule.synonyms
            ]

            for phrase in phrases:
                if phrase.lower() not in query:
                    continue

                existing = matches.get(rule.capability)

                # keep the strong match
                if existing is None or existing.confidence < rule.weight:
                    matches[rule.capability] = CapabilityMatch(
                        capability=rule.capability,
                        confidence=rule.weight,
                        matched_phrase=phrase,
                        rule_priority=rule.priority
                    )

        # fallback
        if not matches:
            return [
                CapabilityMatch(
                    capability=Capability.ADVISOR.value,
                    confidence=0.10,
                    matched_phrase="fallback",
                    rule_priority=999
                )
            ]
        
        return sorted(matches.values(), key= lambda match: (-match.confidence, match.rule_priority, match.capability.value))
