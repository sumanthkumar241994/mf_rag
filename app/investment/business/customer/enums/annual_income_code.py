from enum import StrEnum


class AnnualIncomeCode(StrEnum):
    BELOW_1_LAKH = "31"
    ONE_TO_FIVE_LAKHS = "32"
    FIVE_TO_TEN_LAKHS = "33"
    TEN_TO_TWENTY_FIVE_LAKHS = "34"
    TWENTY_FIVE_LAKHS_TO_ONE_CRORE = "35"
    ABOVE_ONE_CRORE = "36"