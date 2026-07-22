from abc import ABC, abstractmethod

from app.prompts.enums import PromptType
from app.prompts.models import Prompt


class BasePromptBuilder(ABC):

    @property
    @abstractmethod
    def type(self) -> PromptType:
        """Unique prompt type."""
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """Current prompt version."""
        ...

    @abstractmethod
    def build(self, **kwargs) -> Prompt:
        """Build the prompt."""
        ...