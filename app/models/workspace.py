from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import List, Optional


@dataclass
class ApplicationInfo:
    """Information about an application."""

    name: str
    executable: str
    document_path: Optional[str] = None


@dataclass
class ExplorerInfo:
    """Information about a File Explorer window."""

    title: str
    path: str


@dataclass
class VSCodeInfo:
    """Information about a VS Code workspace."""

    title: str
    executable: str
    workspace_name: str
    workspace_path: str


@dataclass
class Workspace:
    """Complete WorkRestore workspace."""

    name: str
    applications: List[ApplicationInfo]
    explorer_windows: List[ExplorerInfo]
    vscode_windows: List[VSCodeInfo]

    def save(self, path: Path) -> None:
        """Save workspace information as JSON."""

        data = {
            "name": self.name,
            "applications": [
                asdict(application)
                for application in self.applications
            ],
            "explorer_windows": [
                asdict(explorer)
                for explorer in self.explorer_windows
            ],
            "vscode_windows": [
                asdict(vscode)
                for vscode in self.vscode_windows
            ],
        }

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                data,
                indent=4,
            ),
            encoding="utf-8",
        )