from dataclasses import dataclass

@dataclass(slots=True)
class DocumentLayout:
    headers: set[str]
    footers: set[str]