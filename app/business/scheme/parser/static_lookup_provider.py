# app/business/scheme/parser/static_lookup_provider.py

from app.business.scheme.enums.lookup_type import LookupType
from app.business.scheme.parser.lookup_provider import LookupProvider


class StaticLookupProvider(LookupProvider):
    """
    Static implementation of LookupProvider.

    Suitable for development and production.
    Can later be replaced with a database-backed implementation
    without changing the parser.
    """

    _LOOKUPS: dict[LookupType, dict[str, str]] = {

        LookupType.CATEGORY: {
            "equity": "Equity",
            "debt": "Debt",
            "Hybrid": "hybrid",
            "Solution": "solution"
        },

        LookupType.SCHEME_TYPE: {
            "liquid": "Liquid Fund",
            "liquid fund": "Liquid Fund",
            "gilt fund": "Gilt Fund",
            "gold": "Gold",
            "fund of funds": "Fund Of Funds",
    },

        LookupType.AMC: {
            "aditya birla sun life": "Aditya Birla Sun Life",
            "axis": "Axis",
            "bandhan": "Bandhan",
            "canara robeco": "Canara Robeco",
            "dsp": "DSP",
            "edelweiss": "Edelweiss",
            "franklin templeton": "Franklin Templeton",
            "hdfc": "HDFC",
            "hsbc": "HSBC",
            "icici": "ICICI",
            "invesco": "Invesco",
            "kotak": "Kotak",
            "mirae asset": "Mirae Asset",
            "motilal oswal": "Motilal Oswal",
            "nippon": "Nippon",
            "parag parikh": "Parag Parikh",
            "quant": "Quant",
            "sbi": "SBI",
            "taurus": "Taurus",
            "trust": "Trust",
            "union": "Union",
            "uti": "UTI",
            "whiteoak": "WhiteOak",
        },

        LookupType.INVESTMENT_OPTION: {
            "growth": "Growth",
            "idcw": "IDCW",
        },
    }

    def lookup(
        self,
        lookup_type: LookupType,
    ) -> dict[str, str]:
        """
        Returns the lookup values for the given lookup type.
        """

        try:
            return self._LOOKUPS[lookup_type]
        except KeyError as ex:
            raise ValueError(
                f"Unsupported lookup type: {lookup_type}"
            ) from ex