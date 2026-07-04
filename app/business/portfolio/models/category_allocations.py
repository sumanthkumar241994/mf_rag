from dataclasses import dataclass

from .category_allocation import CategoryAllocation


@dataclass(slots=True)
class CategoryAllocations:
    equity: CategoryAllocation
    debt: CategoryAllocation
    hybrid: CategoryAllocation
    solution: CategoryAllocation
    others: CategoryAllocation