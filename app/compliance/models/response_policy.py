from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ResponsePolicy:
    required_disclaimers: dict[str, dict[str, bool]]
    required_sections: dict[str, dict[str, bool]]
    response_rules: dict[str, bool]