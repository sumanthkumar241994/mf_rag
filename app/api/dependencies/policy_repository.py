from app.compliance.loader.policy_loader import PolicyLoader
from app.compliance.repository.policy_repository import PolicyRepository


def get_policy_repository() -> PolicyRepository:
    return PolicyRepository(
        loader=PolicyLoader()
    )