from dataclasses import dataclass

@dataclass(slots=True)
class SchemeMetaData:
    scheme_name: str | None = None
    amc_name: str | None = None

