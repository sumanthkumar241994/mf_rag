from dataclasses import dataclass

@dataclass(slots=True)
class TOCExtractionResult:
    found: bool

    titles: list[str]

    toc_start_page: int | None = None

    toc_end_page: int | None = None