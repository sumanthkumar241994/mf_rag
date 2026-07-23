from app.observability.tracing import trace_step
from app.workflows.advisor.advisor_state import AdvisorState
from app.business.advisor.models.planner_result import PlannerResult
from app.business.advisor.planner.classifiers.capability_classifier import CapabilityClassifier
from app.business.advisor.planner.classifiers.intent_classifier import IntentClassifier
from app.business.advisor.planner.planner import Planner
from app.business.advisor.planner.tool_mapper import ToolMapper


class DeterministicPlanner(Planner):
    def __init__(
        self,
        intent_classifier: IntentClassifier,
        capability_classifier: CapabilityClassifier,
        tool_mapper: ToolMapper
    ):
        self._intent_classifier = intent_classifier
        self._capability_classifier = capability_classifier
        self._tool_mapper = tool_mapper
    
    @trace_step(
        "deterministic_planner",
        input_mapper=lambda self, state: {
            "query": state.request.query,
        },
        output_mapper=lambda result: {
            "intent": result.intent.value,
            "capabilities": [
                {
                    "capability": c.capability.value,
                    "confidence": c.confidence,
                }
                for c in result.capabilities
            ],
            "selected_tools": [
                tool.value for tool in result.selected_tools
            ],
            "confidence": result.confidence,
            "reasoning": result.reasoning,
        },
        metadata_mapper=lambda result: {
            "planner": "deterministic",
        },
    )
    async def plan(self, state: AdvisorState) -> PlannerResult:
        query = state.request.query

        # intent 
        intent = self._intent_classifier.classify(query)

        # Capabilities
        capabilities = self._capability_classifier.classify(query, intent)

        #tools
        selected_tools = self._tool_mapper.map(capabilities)

        # planner reasoning
        reasoning = ", ".join(f"{match.capability.value} ← '{match.matched_phrase}'" for match in capabilities)

        return PlannerResult(
            intent=intent,
            capabilities=capabilities,
            selected_tools=selected_tools,
            confidence=1.0,
            reasoning=reasoning
        )