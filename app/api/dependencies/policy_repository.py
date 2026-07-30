from app.compliance.loader.policy_loader import PolicyLoader
from app.compliance.repository.policy_repository import PolicyRepository

_policy_repository: PolicyRepository | None = None

def get_policy_repository() -> PolicyRepository:
    global _policy_repository

    if _policy_repository is None:
        _policy_repository = PolicyRepository(
            loader=PolicyLoader()
        )

    return _policy_repository