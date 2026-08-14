from pathlib import Path
from typing import Any, Dict

from app.adapters.base import ApplicationAdapter


class VSCodeAdapter(ApplicationAdapter):
    """Adapter for Microsoft Visual Studio Code."""

    def can_handle(self, process_name: str) -> bool:
        return process_name.lower() == "code.exe"

    def capture(self, process: Any) -> Dict[str, Any]:
        executable = process.info.get("exe", "")

        return {
            "type": "vscode",
            "name": "Visual Studio Code",
            "executable": executable,
        }

    def restore(self, context: Dict[str, Any]) -> bool:
        executable = context.get("executable")

        if not executable:
            return False

        if not Path(executable).exists():
            return False

        return True