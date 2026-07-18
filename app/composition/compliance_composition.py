from app.compliance.loader.policy_loader import PolicyLoader
from app.compliance.repository.policy_repository import PolicyRepository


class ComplianceComposition:

    def __init__(self):

        self.policy_loader = PolicyLoader()

        self.policy_repository = PolicyRepository(
            loader=self.policy_loader,
        )