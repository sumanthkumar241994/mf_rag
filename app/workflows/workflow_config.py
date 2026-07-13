from app.workflows.advisor.advisor_state import AdvisorState
from langchain_core.runnables import RunnableConfig

class WorkflowConfig:

    @staticmethod
    def config(
        state: AdvisorState,
    ) -> RunnableConfig:
        return {
            "configurable": {
                "thread_id": state.request.conversation_id,
            }
        }

    @staticmethod
    def thread_id(
        state: AdvisorState,
    ) -> str:
        return str(state.request.conversation_id)