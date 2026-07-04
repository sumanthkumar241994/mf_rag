from app.business.advisor.enums.capabilities import Capability
from app.common.exceptions.business_exception import BusinessException

class ToolException(BusinessException):
    """Base exception for all tool-related errors."""
    pass


class DuplicateToolRegistrationException(ToolException):

    def __init__(self, tool_name: str):
        super().__init__(
            message=f"Tool '{tool_name}' is already registered.",
            code="duplicate_tool_registration",
        )


class ToolNotRegisteredException(ToolException):

    def __init__(self, tool_name: str):
        super().__init__(
            message=f"Tool '{tool_name}' is not registered.",
            code="tool_not_registered",
        )


class ToolDisabledException(ToolException):

    def __init__(self, tool_name: str):
        super().__init__(
            message=f"Tool '{tool_name}' is disabled.",
            code="tool_disabled",
        )


class CapabilityNotSupportedException(ToolException):

    def __init__(self, capability: Capability):
        super().__init__(
            message=(
                f"No tool registered for capability "
                f"'{capability.value}'."
            ),
            code="capability_not_supported",
        )


class ToolExecutionException(ToolException):

    def __init__(
        self,
        tool_name: str,
        message: str,
    ):
        super().__init__(
            message=(
                f"Tool '{tool_name}' execution failed: "
                f"{message}"
            ),
            code="tool_execution_failed",
        )


class ToolTimeoutException(ToolException):

    def __init__(self, tool_name: str):
        super().__init__(
            message=f"Tool '{tool_name}' timed out.",
            code="tool_timeout",
        )


class ToolValidationException(ToolException):

    def __init__(
        self,
        tool_name: str,
        message: str,
    ):
        super().__init__(
            message=(
                f"Invalid request for tool "
                f"'{tool_name}': {message}"
            ),
            code="tool_validation_failed",
        )