from pathlib import Path
from typing import Any, Dict

from app.adapters.base import ApplicationAdapter


class TerminalAdapter(ApplicationAdapter):
    """Adapter for Windows Terminal."""

    TERMINAL_NAMES = {
        "windowsterminal.exe",
        "wt.exe",
    }

    def can_handle(self, process_name: str) -> bool:
        return process_name.lower() in self.TERMINAL_NAMES

    def capture(self, process: Any) -> Dict[str, Any]:
        executable = process.info.get("exe", "")
        working_directory = (
            process.info.get("cwd") or ""
        )

        return {
            "type": "terminal",
            "name": "Windows Terminal",
            "executable": executable,
            "working_directory": working_directory,
        }

    def restore(self, context: Dict[str, Any]) -> bool:
        executable = context.get("executable")

        if not executable:
            return False

        return Path(executable).exists()