

from app.business.advisor.enums.tool_type import ToolType
from app.langfuse.models.generation_context import GenerationContext
from app.langfuse.models.observation import Observation
from app.langfuse.models.planner_context import PlannerContext
from app.langfuse.models.prompt_context import PromptContext
from app.langfuse.models.retrieval_context import RetrievalContext, RetrievedChunk
from app.langfuse.models.trace import Trace
from app.langfuse.models.trace_context import TraceContext


class TraceContextBuilder:

    def build(
        self,
        trace: Trace,
    ) -> TraceContext:

        observations = trace.observations

        spans: dict[str, Observation] = {}
        generations: list[Observation] = []

        for observation in observations:

            if observation.type == "SPAN":
                spans[observation.name] = observation

            elif observation.type == "GENERATION":
                generations.append(observation)

        advisor_span = spans.get("advisor_stream_chat")
        llm_planner_span = spans.get("llm_planner")
        deterministic_planner_span = spans.get("deterministic_planner")
        prompt_builder_span = spans.get("prompt_builder")

        planner_generation = self._find_generation(
            generations,
            llm_planner_span.id if llm_planner_span else None,
        )

        advisor_generation = self._find_generation(
            generations,
            advisor_span.id if advisor_span else None,
        )

        planner = self._build_planner(
            llm_planner_span,
            deterministic_planner_span,
        )

        return TraceContext(
            trace_id=trace.id,
            planner=planner,
            prompt=self._build_prompt(prompt_builder_span),
            retrieval=self._build_retrieval(spans),
            planner_generation=self._build_generation(
                planner_generation,
            ),
            advisor_generation=self._build_generation(
                advisor_generation,
            ),
        )

    def _find_generation(
        self,
        generations: list[Observation],
        parent_id: str | None,
    ) -> Observation | None:

        if parent_id is None:
            return None

        for generation in generations:
            if generation.parent_observation_id == parent_id:
                return generation

        return None

    def _build_planner(
        self,
        llm_planner: Observation | None,
        deterministic_planner: Observation | None,
    ) -> PlannerContext | None:

        planner = deterministic_planner or llm_planner

        if planner is None:
            return None

        output = planner.output or {}

        return PlannerContext(
            intent=output.get("intent"),
            confidence=output.get("confidence"),
            reasoning=output.get("reasoning"),
            selected_tools=output.get("selected_tools", []),
            capabilities=output.get("capabilities", []),
        )

    def _build_prompt(
        self,
        prompt_builder: Observation | None,
    ) -> PromptContext | None:

        if prompt_builder is None:
            return None

        output = prompt_builder.output or {}

        return PromptContext(
            system_prompt_length=output.get("system_prompt_length"),
            user_prompt_length=output.get("user_prompt_length"),
            total_prompt_length=output.get("total_prompt_length"),
        )

    # def _build_retrieval(
    #     self,
    #     spans: dict[str, Observation],
    # ) -> RetrievalContext | None:

    #     tools = []

    #     for span in spans.values():

    #         metadata = span.metadata or {}

    #         tool = metadata.get("tool")

    #         if tool:
    #             tools.append(tool)

    #     if not tools:
    #         return None

    #     return RetrievalContext(
    #         tools=tools,
    #     )
    def _build_retrieval(
    self,
    spans: dict[str, Observation],
    ) -> RetrievalContext | None:

        retrieval_span = None

        for span in spans.values():
            metadata = span.metadata or {}

            if metadata.get("tool") == ToolType.DOCUMENT_SEARCH.value:
                retrieval_span = metadata
                break

        if retrieval_span is None:
            return None

        return RetrievalContext(
            tool=retrieval_span.get("tool"),
            query=retrieval_span.get("query"),
            chunk_count=retrieval_span.get("chunk_count", 0),
            truncated=retrieval_span.get("truncated", False),
            chunks=[
                RetrievedChunk(
                    chunk_id=c.get("chunk_id"),
                    document_id=c.get("document_id"),
                    document_name=c.get("document_name"),
                    content=c.get("content"),
                    score=c.get("score"),
                )
                for c in retrieval_span.get("chunks", [])
            ],
        )


    def _build_generation(
    self,
    generation: Observation | None,
    ) -> GenerationContext | None:

        if generation is None:
            return None

        usage = generation.usage
        cost_details = generation.cost_details

        metadata = generation.metadata or {}
        prompt = generation.input or {}

        return GenerationContext(
            model=generation.model,
            system_prompt=prompt.get("system_prompt"),
            user_prompt=prompt.get("user_prompt"),
            response=generation.output,
            finish_reason=metadata.get("finish_reason"),
            input_tokens=usage["input"] if usage else 0,
            output_tokens=usage["output"] if usage else 0,
            total_tokens=usage["total"] if usage else 0,
            latency_ms=metadata.get("latency_ms"),
            first_token_latency_ms=metadata.get("first_token_latency_ms"),
            total_cost=cost_details["total"] if cost_details else 0.0,
            metadata=metadata,
        )
