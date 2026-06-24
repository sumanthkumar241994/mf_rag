# app/workflows/states/advisor_state.py

from typing import TypedDict, NotRequired

from app.schemas.responses.retrieval import RetrievedChunk
from app.schemas.responses.advisor import SourceResponse

class AdvisorState(TypedDict):
    query: str
    chunks: NotRequired[list[RetrievedChunk]]
    context: NotRequired[str]
    sources: NotRequired[list[SourceResponse]]
    answer: NotRequired[str]