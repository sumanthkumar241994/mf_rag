from typing import Any

from langfuse.api.commons.types.observation import Observation as LangfuseObservation
from langfuse.api.commons.types.trace_with_full_details import TraceWithFullDetails 

from app.langfuse.models.observation import Observation
from app.langfuse.models.trace import Trace


class TraceMapper:

    def map(
        self,
        trace: TraceWithFullDetails,
    ) -> Trace:

        return Trace(
            id=trace.id,
            name=trace.name,
            timestamp=trace.timestamp,
            input=trace.input,
            output=trace.output,
            metadata=self._to_dict(trace.metadata),
            latency=trace.latency,
            total_cost=trace.total_cost,
            observations=[
                self._map_observation(observation)
                for observation in trace.observations
            ],
        )

    def _map_observation(
        self,
        observation: LangfuseObservation,
    ) -> Observation:

        return Observation(
            id=observation.id,
            trace_id=observation.trace_id,
            type=observation.type,
            name=observation.name,
            parent_observation_id=observation.parent_observation_id,
            start_time=observation.start_time,
            end_time=observation.end_time,
            input=observation.input,
            output=observation.output,
            metadata=self._to_dict(observation.metadata),
            model=observation.model,
            usage=self._to_dict(observation.usage),
            usage_details=self._to_dict(observation.usage_details),
            cost_details=self._to_dict(observation.cost_details),
            latency=observation.latency,
        )

    @staticmethod
    def _to_dict(value: Any) -> dict[str, Any]:
        if value is None:
            return {}

        if isinstance(value, dict):
            return value

        if hasattr(value, "dict"):
            return value.dict()

        if hasattr(value, "model_dump"):
            return value.model_dump()

        return dict(value)