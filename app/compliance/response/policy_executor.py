from __future__ import annotations

from collections.abc import Sequence

from app.compliance.response.streaming.processing_request import ProcessingRequest
from app.compliance.response.streaming.processing_result import ProcessingResult
from app.compliance.response.validators.base import (
    ResponseComplianceValidator,
)


class PolicyExecutor:

    def __init__(self, validators: list[ResponseComplianceValidator]) -> None:
        self._validators = validators

    async def execute(
        self,
        request: ProcessingRequest,
    ) -> ProcessingResult:

        current_request = request
        findings = []

        for validator in self._validators:

            result = await validator.process(current_request)

            findings.extend(result.findings)

            if result.blocked:
                return ProcessingResult.failure(
                    request=result.request,
                    findings=findings,
                    reason=result.reason,
                )

            current_request = result.request

        return ProcessingResult.success(
            request=current_request,
            findings=findings,
        )