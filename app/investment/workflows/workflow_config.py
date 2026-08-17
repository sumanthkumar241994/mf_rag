from app.investment.workflows.investment_state import InvestmentState
from app.workflows.advisor.advisor_state import AdvisorState
from langchain_core.runnables import RunnableConfig

class WorkflowConfig:

    @staticmethod
    def config(
        state: InvestmentState,
    ) -> RunnableConfig:
        return {
            "configurable": {
                "thread_id": WorkflowConfig.thread_id(state)
            }
        }

    @staticmethod
    def thread_id(
        state: InvestmentState,
    ) -> str:
        return f"investment_purchase:{state.request.conversation_id}"