from collections import defaultdict

from app.business.advisor.enums.intent import Intent
from app.business.advisor.planner.rules.capability_rules import CAPABILITY_RULES
from app.prompts.planner.planner_prompt import (
    SYSTEM_PROMPT,
    OUTPUT_SCHEMA,
)
from app.dtos.llm.llm_request import LLMRequest
from app.workflows.advisor.advisor_state import AdvisorState


class PlannerPromptBuilder:

    def build(self, state: AdvisorState) -> LLMRequest:

        system_prompt = "\n\n".join(
            [
                SYSTEM_PROMPT,
                self._build_intents(),
                self._build_capabilities(),
                OUTPUT_SCHEMA
            ]
        )

        user_prompt = f"""
            <customer_query>

            "Query": {state.request.query}

            "Delegation Context": {state.request.delegation}

            </customer_query>
            """.strip()

        return LLMRequest(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.0,
            max_tokens=500,
        )

    def _build_intents(self) -> str:

        lines = ["Supported Intents"]

        for intent in Intent:
            lines.append(f"- {intent.value}")

        return "\n".join(lines)

    def _build_capabilities(self) -> str:
        capability_map: dict = defaultdict(
            lambda: {
                "keywords": set(),
                "examples": set(),
            }
        )

        for rule in CAPABILITY_RULES:

            capability_map[rule.capability]["keywords"].update(rule.keywords)
            capability_map[rule.capability]["keywords"].update(rule.synonyms)
            capability_map[rule.capability]["examples"].update(rule.examples)

        lines = ["Supported Capabilities"]

        for capability in sorted(
            capability_map.keys(),
            key=lambda c: c.value,
        ):
            lines.append("")
            lines.append(capability.value)

            keywords = sorted(capability_map[capability]["keywords"])
            examples = sorted(capability_map[capability]["examples"])

            if keywords:
                lines.append("Keywords:")
                for keyword in keywords:
                    lines.append(f"- {keyword}")

            if examples:
                lines.append("Examples:")
                for example in examples:
                    lines.append(f"- {example}")

        return "\n".join(lines)