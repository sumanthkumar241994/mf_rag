from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True, frozen=True)
class SectorHolding:
    sector: str
    allocation: Decimal