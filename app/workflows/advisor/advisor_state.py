# app/workflows/states/advisor_state.py

from typing import NotRequired

from app.schemas.responses.retrieval import RetrievedChunk
from app.schemas.responses.advisor import SourceResponse
from app.workflows.common.base_state import BaseWorkflowState

class AdvisorState(BaseWorkflowState):
    chunks: NotRequired[list[RetrievedChunk]]
    context: NotRequired[str]
    sources: NotRequired[list[SourceResponse]]
    answer: NotRequired[str]