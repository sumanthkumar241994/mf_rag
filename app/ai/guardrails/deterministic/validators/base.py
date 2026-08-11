from abc import ABC, abstractmethod

from app.ai.guardrails.deterministic.models.guardrail_result import GuardRailResult
from app.dtos.request_context import RequestContext

from collections.abc import Mapping, Sequence

class GuardRailValidator(ABC):

    @abstractmethod
    async def validate(
        self,
        request: RequestContext,
    ) -> GuardRailResult:
        pass

    def extract_text(
        self,
        request_context: RequestContext,
    ) -> list[str]:

        texts: list[str] = []

        if request_context.query:
            texts.append(request_context.query)

        if request_context.workflow_resume is not None:
            texts.extend(
                self._extract_strings(
                    request_context.workflow_resume,
                )
            )

        return texts

    def _extract_strings(
        self,
        value,
    ) -> list[str]:

        if value is None:
            return []

        if isinstance(value, str):
            return [value]

        if isinstance(value, Mapping):
            result: list[str] = []
            for v in value.values():
                result.extend(
                    self._extract_strings(v)
                )
            return result

        if (
            isinstance(value, Sequence)
            and not isinstance(value, (str, bytes))
        ):
            result: list[str] = []
            for item in value:
                result.extend(
                    self._extract_strings(item)
                )
            return result

        return []