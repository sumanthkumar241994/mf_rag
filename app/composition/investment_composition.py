

from langgraph.checkpoint.base import BaseCheckpointSaver
from app.agents.investment_agent import InvestmentAgent
from app.composition.mcp_clients.customer_client_composition import CustomerClientComposition
from app.composition.mcp_clients.otp_client_composition import OTPClientComposition
from app.investment.business.execution.complete_action_handler import CompletionActionHandler
from app.investment.business.execution.completion_stage import CompletionStage
from app.investment.business.execution.customer.builder.fatca_data_collection_builder import FatcaCollectionBuilder
from app.investment.business.execution.customer.builder.nominee_data_collection_builder import NomineeCollectionBuilder
from app.investment.business.execution.customer.customer_action_handler_registry import CustomerActionHandlerRegistry
from app.investment.business.execution.customer.customer_data_collection_registry import CustomerDataCollectionBuilderRegistry
from app.investment.business.execution.customer.handlers.customer_action_handler import CustomerActionHandler
from app.investment.business.execution.customer.handlers.fatca_update_action_handler import FatcaUpdateActionHandler
from app.investment.business.execution.customer.handlers.nominee_update_action_handler import NomineeUpdateActionHandler
from app.investment.business.execution.customer.planners.customer_collection_stage import CustomerCollectionStage
from app.investment.business.execution.customer.planners.customer_sync_stage import CustomerSyncStage
from app.investment.business.execution.customer.planners.customer_update_stage import CustomerActionStage
from app.investment.business.execution.eligibility.eligibility_action_handler_registry import EligibilityActionHandlerRegistry
from app.investment.business.execution.eligibility.handlers.data_collection_interrupt_handler import DataCollectionInterruptHandler
from app.investment.business.execution.eligibility.handlers.eligibility_action_handler import EligibilityActionHandler
from app.investment.business.execution.eligibility.planners.eligibility_stage import EligibilityStage
from app.investment.business.execution.eligibility_action_mapper import EligibilityActionMapper
from app.investment.business.execution.execution_engine import ExecutionEngine
from app.investment.business.execution.planner.rule_based_execution_planner import RuleBasedExecutionPlanner
from app.investment.services.eligibility_service import EligibilityService
from app.investment.workflows.investment_workflow import InvestmentWorkflow
from app.investment.workflows.nodes import verification_node
from app.investment.workflows.nodes.customer_node import CustomerNode
from app.investment.workflows.nodes.data_collection_node import DataCollectionNode
from app.investment.workflows.nodes.eligbility_node import EligibilityNode
from app.investment.workflows.nodes.verification_node import VerificationNode
from app.investment.workflows.nodes.verification_prepare_node import VerificationPrepareNode
from app.investment.workflows.nodes.verification_wait_node import VerificationWaitNode
from app.mcp.client.mcp_client import MCPClient


class InvestmentComposition:
    """
    Composition root for the Investment workflow.

    Responsible only for wiring the application together.
    """

    def __init__(
        self,
        mcp: MCPClient,
        checkpointer: BaseCheckpointSaver,
    ):
        
        self.customer_client = CustomerClientComposition(mcp)

        self.otp_client = OTPClientComposition(mcp)


        # Customer
        customer_action_handler = CustomerActionHandler(customer_client=self.customer_client.client)
        nominee_action_handler = NomineeUpdateActionHandler(customer_client=self.customer_client.client)
        fatca_action_handler = FatcaUpdateActionHandler(customer_client=self.customer_client.client)
        customer_registry = CustomerActionHandlerRegistry(
            customer_action_handler=customer_action_handler,
            nominee_action_handler=nominee_action_handler,
            fatca_action_handler=fatca_action_handler
        )

        customer_builder_registry = CustomerDataCollectionBuilderRegistry(
            nominee_builder=NomineeCollectionBuilder(),
            fatca_builder=FatcaCollectionBuilder()
        )

        customer_planner = RuleBasedExecutionPlanner(
            stages=[
                CustomerSyncStage(),
                CustomerCollectionStage(),
                CustomerActionStage(),
            ],
        )

        customer_engine = ExecutionEngine(
            planner=customer_planner,
            action_handler_registry=customer_registry,
        )

        self.customer_node = CustomerNode(
            engine=customer_engine,
        )
        
        # Eligibility
        eligibility_registry = EligibilityActionHandlerRegistry(
            eligibility_action_handler=EligibilityActionHandler(),
            data_collection_interrupt_handler=DataCollectionInterruptHandler(EligibilityActionMapper()),
        )
        
        eligibility_service = EligibilityService()
        eligibility_planner = RuleBasedExecutionPlanner(
            stages=[
                EligibilityStage(eligibility_service),
            ],
        )

        eligibility_engine = ExecutionEngine(
            planner=eligibility_planner,
            action_handler_registry=eligibility_registry,
        )

        self.eligibility_node = EligibilityNode(
            engine=eligibility_engine,
        )

        self.verification_prepare_node = VerificationPrepareNode(
            otp_client=self.otp_client.client
        )

        self.verification_wait_node = VerificationWaitNode(otp_client=self.otp_client.client)

        self.data_collection_node = DataCollectionNode(customer_builder_registry)
        self.workflow = InvestmentWorkflow(
            customer_node=self.customer_node,
            eligibility_node=self.eligibility_node,
            data_collection_node=self.data_collection_node,
            verification_prepare_node=self.verification_prepare_node,
            verification_wait_node=self.verification_wait_node,
            checkpointer=checkpointer,
        )

        self.agent = InvestmentAgent(
            investment_workflow=self.workflow
        )