from app.common.exceptions.business_exception import BusinessException


class FeedbackException(BusinessException):
    """Base exception for feedback domain."""


class FeedbackMessageNotFoundException(FeedbackException):

    def __init__(self) -> None:
        super().__init__(
            message="The requested message was not found.",
            code="FEEDBACK_MESSAGE_NOT_FOUND",
        )


class FeedbackUnauthorizedException(FeedbackException):

    def __init__(self) -> None:
        super().__init__(
            message="You are not authorized to submit feedback for this message.",
            code="FEEDBACK_UNAUTHORIZED",
        )


class FeedbackNotAllowedException(FeedbackException):

    def __init__(self) -> None:
        super().__init__(
            message="Feedback can only be submitted for assistant messages.",
            code="FEEDBACK_NOT_ALLOWED",
        )


class InvalidFeedbackException(FeedbackException):

    def __init__(self) -> None:
        super().__init__(
            message="The feedback request is invalid.",
            code="INVALID_FEEDBACK",
        )


class InvalidFeedbackSignalException(InvalidFeedbackException):

    def __init__(self) -> None:
        super().__init__()
        self.code = "INVALID_FEEDBACK_SIGNAL"
        self.message = "The feedback signal is invalid."


class InvalidFeedbackReasonException(InvalidFeedbackException):

    def __init__(self) -> None:
        super().__init__()
        self.code = "INVALID_FEEDBACK_REASON"
        self.message = "The feedback reason is invalid."


class InvalidFeedbackCommentException(InvalidFeedbackException):

    def __init__(self) -> None:
        super().__init__()
        self.code = "INVALID_FEEDBACK_COMMENT"
        self.message = "The feedback comment is invalid."