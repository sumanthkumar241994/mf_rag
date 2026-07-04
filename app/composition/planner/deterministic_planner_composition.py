from app.business.advisor.planner.classifiers.capability_classifier import CapabilityClassifier
from app.business.advisor.planner.classifiers.intent_classifier import IntentClassifier
from app.business.advisor.planner.deterministic_planner import DeterministicPlanner
from app.business.advisor.planner.planner import Planner
from app.business.advisor.planner.tool_mapper import ToolMapper


class DeterministicPlannerComposition:
    def __init__(self):
        # Classifiers
        self.intent_classifier = IntentClassifier()
        self.capability_classifier = CapabilityClassifier()
        self.tool_mapper = ToolMapper()

        # Planner
        self.planner = DeterministicPlanner(
            intent_classifier=self.intent_classifier,
            capability_classifier=self.capability_classifier,
            tool_mapper=self.tool_mapper
        )