from abc import ABC, abstractmethod
from typing import Any, Dict


class ApplicationAdapter(ABC):
    """Base class for application-specific workspace adapters."""

    @abstractmethod
    def can_handle(self, process_name: str) -> bool:
        """Return True if this adapter handles the process."""

    @abstractmethod
    def capture(self, process: Any) -> Dict[str, Any]:
        """Capture application-specific context."""

    @abstractmethod
    def restore(self, context: Dict[str, Any]) -> bool:
        """Restore application-specific context."""