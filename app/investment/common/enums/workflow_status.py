from enum import StrEnum


class WorkflowStatus(StrEnum):
    """
    Current status of a workflow execution.
    """

    # Workflow created but not yet started.
    PENDING = "pending"

    # Waiting for customer interaction (OTP, bank, nominee, FATCA, etc.).
    INTERRUPTED = "interrupted"

    # Backend processing is in progress.
    PROCESSING = "processing"

    # Successfully completed.
    COMPLETED = "completed"

    # Permanently failed.
    FAILED = "failed"

    # Cancelled by customer or system.
    CANCELLED = "cancelled"