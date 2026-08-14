from typing import List

from app.adapters.base import ApplicationAdapter
from app.adapters.terminal import TerminalAdapter
from app.adapters.vscode import VSCodeAdapter


def get_adapters() -> List[ApplicationAdapter]:
    """Return all registered application adapters."""

    return [
        VSCodeAdapter(),
        TerminalAdapter(),
    ]


def get_adapter(
    process_name: str,
) -> ApplicationAdapter | None:
    """Find an adapter for a process."""

    for adapter in get_adapters():
        if adapter.can_handle(process_name):
            return adapter

    return None