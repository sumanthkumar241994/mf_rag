from app.business.advisor.enums.capabilities import Capability
from app.business.advisor.models.advisor_error import AdvisorError
from app.business.common.models.gateway_result import GatewayResult
from app.business.common.services.base_workflow_service import BaseWorkflowService
from app.business.scheme.gateways.scheme_gateway import SchemeGateway
from app.business.scheme.mappers.scheme_mapper import SchemeMapper
from app.business.scheme.models import scheme_query
from app.business.scheme.models.scheme_details import SchemeDetails
from app.business.scheme.models.scheme_query import SchemeQuery
from app.business.scheme.models.scheme_summary import SchemeSummary
from app.business.scheme.parsers.scheme_query_parser import SchemeQueryParser
from app.business.scheme.scheme_resolver import SchemeResolver
from app.infrastructure.api_client.models import GateWayRequestContext
from app.workflows.advisor.advisor_state import AdvisorState
from app.workflows.workflow.models.workflow_execution import WorkflowExecution
from app.workflows.workflow.service.workflow_service import WorkflowService


class SchemeService(BaseWorkflowService[SchemeDetails]):
    def __init__(
        self,
        scheme_gateway: SchemeGateway,
        scheme_mapper: SchemeMapper,
        scheme_query_parser: SchemeQueryParser,
        scheme_resolver: SchemeResolver,
        workflow_service: WorkflowService
    ):
        super().__init__(workflow_service)

        self._scheme_gateway = scheme_gateway
        self._scheme_mapper = scheme_mapper
        self._scheme_query_parser = scheme_query_parser
        self._scheme_resolver = scheme_resolver
        self._workflow_service = workflow_service

    async def execute(
        self,
        state: AdvisorState,
    ) -> WorkflowExecution[SchemeDetails]:
        """
        Retrieves scheme information and enriches AdvisorState.
        """
        scheme_query = self._parse_query(state)
        gateway_context = self._build_gateway_context(state)
        search_results = await self._search_schemes(
            state=state,
            query=scheme_query,
            gateway_context=gateway_context,
        )

        if search_results is None:
            return

        resolved_schemes = self._resolve_schemes(
            search_results=search_results,
            query=scheme_query,
        )

        schemes = await self._fetch_scheme_details(
            state=state,
            summaries=resolved_schemes,
            gateway_context=gateway_context,
        )

        if schemes is None:
            return

        execution = self._create_workflow_execution(
            state=state,
            capability=Capability.INVESTMENT,
            result=schemes,
            complete=True
        )

        if schemes is None:
            return execution

        state.workflow_execution = execution
        state.schemes = schemes

        return execution
    # ------------------------------------------------------------------ #

    def _parse_query(
        self,
        state: AdvisorState,
    ) -> SchemeQuery:

        parser_result = self._scheme_query_parser.parse(
            state.request.query
        )

        state.scheme_query = parser_result.query
        state.metadata["scheme_parser"] = parser_result

        return parser_result.query

    # ------------------------------------------------------------------ #

    def _build_gateway_context(
        self,
        state: AdvisorState,
    ) -> GateWayRequestContext:

        return GateWayRequestContext(
            trace_id=state.trace_id,
            conversation_id=state.request.conversation_id,
            customer_id=state.request.customer_id,
        )

    # ------------------------------------------------------------------ #

    async def _search_schemes(
        self,
        state: AdvisorState,
        query: SchemeQuery,
        gateway_context: GateWayRequestContext,
    ) -> list[list[SchemeSummary]] | None:

        search_results: list[list[SchemeSummary]] = []

        # Recommendation query
        if query.recommendation:

            result: GatewayResult = await self._scheme_gateway.search(
                context=gateway_context,
                request=query,
            )

            if not result.success:
                state.add_error(
                    AdvisorError.from_gateway(
                        error=result.error,
                        source="scheme_gateway",
                    )
                )
                return None

            search_results.append(
                self._scheme_mapper.to_summary_list(result.data)
            )

            return search_results


        search_query = query.clone_for_scheme(
            query.q
        )

        result = await self._scheme_gateway.search(
            context=gateway_context,
            request=search_query,
        )

        if not result.success:
            state.add_error(
                AdvisorError.from_gateway(
                    error=result.error,
                    source="scheme_gateway",
                )
            )
            return None

        search_results.append(
            self._scheme_mapper.to_summary_list(result.data)
        )

        return search_results


    def _resolve_schemes(
        self,
        search_results: list[list[SchemeSummary]],
        query: SchemeQuery,
    ) -> list[SchemeSummary]:

        return self._scheme_resolver.resolve(
            search_results=search_results,
            query=query,
        )


    async def _fetch_scheme_details(
        self,
        state: AdvisorState,
        summaries: list[SchemeSummary],
        gateway_context: GateWayRequestContext,
    ) -> list[SchemeDetails] | None:

        schemes: list[SchemeDetails] = []

        for summary in summaries:

            result = await self._scheme_gateway.get_scheme_details(
                context=gateway_context,
                scheme_id=summary.id,
            )

            if not result.success:
                state.add_error(
                    AdvisorError.from_gateway(
                        error=result.error,
                        source="scheme_gateway",
                    )
                )
                return None

            schemes.append(
                self._scheme_mapper.to_details(
                    result.data
                )
            )

        return schemes