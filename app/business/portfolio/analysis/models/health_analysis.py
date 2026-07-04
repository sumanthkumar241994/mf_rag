from dataclasses import dataclass

@dataclass(slots=True)
class HealthAnalysis:
    health_score: int
    health_rating: str