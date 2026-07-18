from pathlib import Path
import re
from re import Pattern

import yaml

from app.compliance.enums.compliance_action import ComplianceAction
from app.compliance.enums.severity import Severity
from app.compliance.exceptions import PolicyLoadError
from app.compliance.models.compliance_policies import CompliancePolicies
from app.compliance.models.prompt_policy import (
    PromptPolicy,
    PromptSystemRequirements,
    PromptLimits,
)
from app.compliance.models.response_policy import (
    ResponsePolicy,
)
from app.compliance.models.prohibited_phrases import (
    ProhibitedPhrase,
    ProhibitedPhrases,
)
from app.compliance.models.regulatory_link import RegulatoryLink
from app.compliance.models.regulatory_links import RegulatoryLinks
from app.core.config import settings

from app.compliance.enums.compliance_action import ComplianceAction
from app.compliance.enums.severity import Severity
from app.compliance.models.prohibited_phrases import ProhibitedPhrases
from app.compliance.models.response_policy import ResponsePolicy

class PolicyLoader:

    def __init__(
        self,
    ):
        self._policy_directory = settings.COMPLIANCE_POLICY_DIRECTORY

    def load(self) -> CompliancePolicies:

        try:
            prompt = self._load_prompt_policy()
            # response = self._load_response_policy()
            prohibited = self._load_prohibited_phrases()
            links = self._load_regulatory_links()

            return CompliancePolicies(
                prompt=prompt,
                prohibited_phrases=prohibited,
                regulatory_links=links,
            )

        except Exception as exc:
            raise PolicyLoadError(
                f"Unable to load compliance policies: {exc}"
            ) from exc

    def _read_yaml(
        self,
        filename: str,
    ) -> dict:

        path = self._policy_directory / filename

        with open(path, "r", encoding="utf-8") as fp:
            return yaml.safe_load(fp)

    def _load_prompt_policy(
        self,
    ) -> PromptPolicy:

        payload = self._read_yaml("prompt_policy.yml")

        return PromptPolicy(
            system_requirements=PromptSystemRequirements(
                **payload["system_requirements"],
            ),
            limits=PromptLimits(
                **payload["limits"],
            ),
        )

    # def _load_response_policy(
    # self,
    # ) -> ResponsePolicy:

    #     payload = self._read_yaml("response_policy.yml")

    #     prohibited_phrases = ProhibitedPhrases(
    #     blocked=[
    #                 ProhibitedPhrase(
    #                     pattern=re.compile(item["pattern"], re.IGNORECASE),
    #                     description=item["description"],
    #                     severity=Severity(item["severity"]),
    #                     action=ComplianceAction(item["action"]),
    #                     replacement=item.get("replacement"),
    #                 )
    #                 for item in payload.get("blocked", [])
    #             ]
    #         )

    #     return ResponsePolicy(
    #         prohibited_phrases=prohibited_phrases,
    #         required_disclaimers=payload.get("required_disclaimers", []),
    #         required_sections=payload.get("required_sections", []),
    #         response_rules=payload.get("response_rules", []),
    #     )

    def _load_prohibited_phrases(
    self,
    ) -> ProhibitedPhrases[Pattern[str]]:

        payload = self._read_yaml(
            "prohibited_phrases.yml",
        )

        return ProhibitedPhrases[Pattern[str]](
            blocked=[
                ProhibitedPhrase(
                    pattern=re.compile(
                        item["pattern"],
                        re.IGNORECASE,
                    ),
                    description=item["description"],
                    severity=Severity(item["severity"]),
                    action=ComplianceAction(item["action"]),
                    replacement=item.get("replacement"),
                )
                for item in payload["blocked"]
            ]
        )

    def _load_regulatory_links(
        self,
    ) -> RegulatoryLinks:

        payload = self._read_yaml(
            "regulatory_links.yml",
        )

        def build_links(section: dict) -> dict[str, RegulatoryLink]:

            return {
                key: RegulatoryLink(
                    title=value["title"],
                    url=value["url"],
                )
                for key, value in section.items()
            }

        return RegulatoryLinks(
            rbi=build_links(payload["rbi"]),
            sebi=build_links(payload["sebi"]),
        )