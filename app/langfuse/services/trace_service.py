from app.langfuse.builders.trace_context_builder import TraceContextBuilder
from app.langfuse.client import LangfuseClient
from app.langfuse.trace_mapper import TraceMapper
from app.langfuse.models.trace_context import TraceContext


class TraceService:

    def __init__(
        self,
        client: LangfuseClient,
        mapper: TraceMapper | None = None,
        builder: TraceContextBuilder | None = None,
    ):
        self._client = client.client
        self._mapper = mapper or TraceMapper()
        self._builder = builder or TraceContextBuilder()

    def get_trace(
        self,
        trace_id: str,
    ) -> TraceContext:
        trace = self._client.api.trace.get(trace_id)

        trace = self._mapper.map(trace)

        return self._builder.build(trace)