from dataclasses import dataclass

from app.compliance.models.regulatory_link import RegulatoryLink


@dataclass(slots=True, frozen=True)
class RegulatoryLinks:
    rbi: dict[str, RegulatoryLink]
    sebi: dict[str, RegulatoryLink]