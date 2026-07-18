from abc import ABC, abstractmethod

from app.compliance.response.streaming.processing_request import ProcessingRequest
from app.compliance.response.streaming.processing_result import ProcessingResult


class ResponseComplianceValidator(ABC):

    @abstractmethod
    async def process(
        self,
        request: ProcessingRequest,
    ) -> ProcessingResult:
        """
        Process the response and return the transformed result.
        """
        raise NotImplementedError