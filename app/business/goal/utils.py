import re
from decimal import Decimal


_AMOUNT_PATTERN = re.compile(
    r"(?:₹\s*)?(\d+(?:\.\d+)?)\s*(crore|cr|lakh|lac|lakhs|lacs|k|thousand|million|billion)?",
    re.IGNORECASE,
)

_YEAR_PATTERN = re.compile(
    r"(\d{1,2})\s*(?:years?|yrs?)",
    re.IGNORECASE,
)

_AGE_PATTERN = re.compile(
    r"(?:age\s*|at\s*)?(\d{2})",
    re.IGNORECASE,
)

_PERCENT_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)\s*%",
    re.IGNORECASE,
)

_RETIREMENT_AGE_PATTERNS = (
    re.compile(
        r"(?:retire|retirement)\s*(?:at|age)?\s*(\d{2})",
        re.IGNORECASE,
    ),
    re.compile(
        r"at\s+(\d{2})\s+(?:years?|yrs?)",
        re.IGNORECASE,
    ),
)

_EXPECTED_RETURN_PATTERNS = (
    re.compile(
        r"(?:return|returns|cagr|growth)\s*(?:of)?\s*(\d+(?:\.\d+)?)\s*%",
        re.IGNORECASE,
    ),
    re.compile(
        r"(\d+(?:\.\d+)?)\s*%\s*(?:return|returns|cagr|growth)",
        re.IGNORECASE,
    ),
)

_INFLATION_PATTERNS = (
    re.compile(
        r"inflation(?:\s*rate)?\s*(?:of)?\s*(\d+(?:\.\d+)?)\s*%",
        re.IGNORECASE,
    ),
    re.compile(
        r"(\d+(?:\.\d+)?)\s*%\s*inflation",
        re.IGNORECASE,
    ),
)


def normalize_query(query: str) -> str:
    return re.sub(r"\s+", " ", query).strip().lower()


def extract_amount(query: str) -> Decimal | None:

    query_lower = query.lower()

    amounts: list[Decimal] = []

    multipliers = {
        "crore": Decimal("10000000"),
        "cr": Decimal("10000000"),
        "lakh": Decimal("100000"),
        "lakhs": Decimal("100000"),
        "lac": Decimal("100000"),
        "lacs": Decimal("100000"),
        "k": Decimal("1000"),
        "thousand": Decimal("1000"),
        "million": Decimal("1000000"),
        "billion": Decimal("1000000000"),
    }

    _AMOUNT_KEYWORDS = {
            "amount",
            "corpus",
            "target",
            "goal",
            "wealth",
            "fund",
            "investment",
            "money",
            "save",
            "saving",
        }

    for match in _AMOUNT_PATTERN.finditer(query):

        value = Decimal(match.group(1).replace(",", ""))

        unit = (match.group(2) or "").lower()

        # No unit like crore/lakh/k
        if not unit:
            if not any(keyword in query_lower for keyword in _AMOUNT_KEYWORDS):
                continue

        multiplier = multipliers.get(
            unit,
            Decimal("1"),
        )

        amounts.append(value * multiplier)

    if not amounts:
        return None

    return max(amounts)


def extract_years(query: str) -> int | None:
    match = _YEAR_PATTERN.search(query)

    if not match:
        return None

    return int(match.group(1))


def extract_age(query: str) -> int | None:
    matches = _AGE_PATTERN.findall(query)

    if not matches:
        return None

    for age in matches:
        age = int(age)

        if 40 <= age <= 80:
            return age

    return None


def extract_percentage(query: str) -> Decimal | None:
    match = _PERCENT_PATTERN.search(query)

    if not match:
        return None

    return Decimal(match.group(1))


def extract_retirement_age(
    query: str,
) -> int | None:
    for pattern in _RETIREMENT_AGE_PATTERNS:
        match = pattern.search(query)

        if match:
            return int(match.group(1))

    return None


def extract_expected_return(
    query: str,
) -> Decimal | None:
    for pattern in _EXPECTED_RETURN_PATTERNS:
        match = pattern.search(query)

        if match:
            return Decimal(match.group(1))

    return None


def extract_inflation_rate(
    query: str,
) -> Decimal | None:
    for pattern in _INFLATION_PATTERNS:
        match = pattern.search(query)

        if match:
            return Decimal(match.group(1))

    return None


def extract_goal_amount(
    query: str,
) -> Decimal | None:
    return extract_amount(query)


def extract_current_corpus(
    query: str,
) -> Decimal | None:
    return extract_amount(query)


def extract_monthly_investment(
    query: str,
) -> Decimal | None:
    return extract_amount(query)


def extract_current_age(
    query: str,
) -> int | None:
    return extract_age(query)


def extract_target_years(
    query: str,
) -> int | None:
    return extract_years(query)


def extract_resume_age(
    answer: str,
) -> int | None:

    match = re.search(r"\b(\d{2})\b", answer)

    if not match:
        return None

    age = int(match.group(1))

    if 40 <= age <= 80:
        return age

    return None