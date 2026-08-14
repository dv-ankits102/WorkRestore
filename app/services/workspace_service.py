from pathlib import Path
from typing import Dict, List, Optional, Set
import json

import psutil

from app.models.workspace import (
    ApplicationInfo,
    ExplorerInfo,
    VSCodeInfo,
    Workspace,
)

from app.services.explorer_service import (
    get_open_explorer_windows,
)

from app.services.vscode_service import (
    get_vscode_windows,
)

from app.services.document_service import (
    get_open_office_documents,
)


# ============================================================
# Workspace Storage
# ============================================================

WORKSPACE_DIRECTORY = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "workspaces"
)


# ============================================================
# Supported Applications
# ============================================================

SUPPORTED_APPLICATIONS = {
    # Browsers
    "chrome.exe",
    "msedge.exe",
    "firefox.exe",
    "brave.exe",
    "opera.exe",
    "opera_gx.exe",
    "vivaldi.exe",

    # Microsoft Office
    "winword.exe",
    "excel.exe",
    "powerpnt.exe",
    "outlook.exe",
    "onenote.exe",
    "msaccess.exe",
    "mspub.exe",

    # Windows
    "notepad.exe",
    "notepad++.exe",
    "write.exe",

    # Development
    "code.exe",
    "devenv.exe",
    "idea64.exe",
    "pycharm.exe",
    "pycharm64.exe",
    "androidstudio.exe",

    # Terminals
    "cmd.exe",
    "powershell.exe",
    "pwsh.exe",
    "windowsterminal.exe",
    "wt.exe",

    # Communication
    "slack.exe",
    "discord.exe",
    "teams.exe",
    "ms-teams.exe",
    "zoom.exe",
    "telegram.exe",
    "whatsapp.exe",

    # Other
    "postman.exe",
    "figma.exe",
    "vlc.exe",
    "spotify.exe",
}


# ============================================================
# Application Capture
# ============================================================
def _capture_applications() -> List[ApplicationInfo]:
    """
    Capture supported user applications.

    Microsoft Office applications include the exact
    currently opened document path when available.
    """

    applications: Dict[
        str,
        ApplicationInfo,
    ] = {}

    # ---------------------------------------------------------
    # 1. Capture normal running applications
    # ---------------------------------------------------------

    for process in psutil.process_iter(
        ["name", "exe"]
    ):
        try:
            process_name = process.info["name"]
            executable = process.info["exe"]

            if not process_name:
                continue

            if not executable:
                continue

            process_name_lower = (
                process_name.lower()
            )

            if (
                process_name_lower
                not in SUPPORTED_APPLICATIONS
            ):
                continue

            executable_key = executable.lower()

            if executable_key in applications:
                continue

            applications[
                executable_key
            ] = ApplicationInfo(
                name=process_name,
                executable=executable,
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    # ---------------------------------------------------------
    # 2. Capture exact Office documents
    # ---------------------------------------------------------

    try:
        office_documents = (
            get_open_office_documents()
        )

        for document in office_documents:

            executable_key = (
                document.executable.lower()
            )

            applications[
                executable_key
            ] = ApplicationInfo(
                name=document.application_name,
                executable=document.executable,
                document_path=document.document_path,
            )

    except Exception:
        # Office detection must never break
        # normal workspace saving.
        pass

    return sorted(
        applications.values(),
        key=lambda application: (
            application.name.lower()
        ),
    )

# ============================================================
# Explorer Capture
# ============================================================

def _capture_explorer_windows() -> List[ExplorerInfo]:
    """
    Capture currently open File Explorer folders.

    Duplicate folder paths are removed.
    """

    explorer_windows: List[
        ExplorerInfo
    ] = []

    seen_paths: Set[str] = set()

    for window in get_open_explorer_windows():

        path = window.path

        if not path:
            continue

        normalized_path = path.lower()

        if normalized_path in seen_paths:
            continue

        seen_paths.add(
            normalized_path
        )

        explorer_windows.append(
            ExplorerInfo(
                title=window.title,
                path=path,
            )
        )

    return explorer_windows


# ============================================================
# VS Code Capture
# ============================================================

def _capture_vscode_windows() -> List[VSCodeInfo]:
    """
    Capture currently open VS Code workspaces.

    Duplicate workspace paths are removed.
    """

    vscode_windows: List[
        VSCodeInfo
    ] = []

    seen_paths: Set[str] = set()

    for window in get_vscode_windows():

        workspace_path = (
            window.workspace_path
        )

        if not workspace_path:
            continue

        normalized_path = (
            workspace_path.lower()
        )

        if normalized_path in seen_paths:
            continue

        seen_paths.add(
            normalized_path
        )

        vscode_windows.append(
            VSCodeInfo(
                title=window.title,
                executable=window.executable,
                workspace_name=(
                    window.workspace_name
                ),
                workspace_path=workspace_path,
            )
        )

    return vscode_windows


# ============================================================
# Application Filtering
# ============================================================

def _filter_applications(
    applications: List[ApplicationInfo],
    selected_names: Optional[Set[str]],
) -> List[ApplicationInfo]:
    """
    Return only applications selected by the user.

    If selected_names is None, all supported
    applications are returned.
    """

    if selected_names is None:
        return applications

    selected = {
        name.lower()
        for name in selected_names
    }

    return [
        application
        for application in applications
        if application.name.lower()
        in selected
    ]


# ============================================================
# Explorer Filtering
# ============================================================

def _filter_explorer(
    explorers: List[ExplorerInfo],
    selected_paths: Optional[Set[str]],
) -> List[ExplorerInfo]:
    """
    Return only Explorer folders selected by the user.
    """

    if selected_paths is None:
        return explorers

    selected = {
        path.lower()
        for path in selected_paths
    }

    return [
        explorer
        for explorer in explorers
        if explorer.path.lower()
        in selected
    ]


# ============================================================
# VS Code Filtering
# ============================================================

def _filter_vscode(
    workspaces: List[VSCodeInfo],
    selected_paths: Optional[Set[str]],
) -> List[VSCodeInfo]:
    """
    Return only VS Code workspaces selected by the user.
    """

    if selected_paths is None:
        return workspaces

    selected = {
        path.lower()
        for path in selected_paths
    }

    return [
        vscode
        for vscode in workspaces
        if vscode.workspace_path.lower()
        in selected
    ]


# ============================================================
# Workspace Capture
# ============================================================

def capture_workspace(
    name: str,
    selected_applications: Optional[
        Set[str]
    ] = None,
    selected_explorer_paths: Optional[
        Set[str]
    ] = None,
    selected_vscode_paths: Optional[
        Set[str]
    ] = None,
) -> Workspace:
    """
    Capture the current Windows workspace.

    Only selected applications, Explorer folders,
    and VS Code workspaces are included.
    """

    if not name or not name.strip():
        raise ValueError(
            "Workspace name cannot be empty."
        )

    workspace_name = name.strip()

    # Capture current state
    applications = (
        _capture_applications()
    )

    explorers = (
        _capture_explorer_windows()
    )

    vscode_workspaces = (
        _capture_vscode_windows()
    )

    # Apply user selections
    applications = _filter_applications(
        applications,
        selected_applications,
    )

    explorers = _filter_explorer(
        explorers,
        selected_explorer_paths,
    )

    vscode_workspaces = _filter_vscode(
        vscode_workspaces,
        selected_vscode_paths,
    )

    return Workspace(
        name=workspace_name,
        applications=applications,
        explorer_windows=explorers,
        vscode_windows=vscode_workspaces,
    )


# ============================================================
# Save Workspace
# ============================================================

def save_workspace(
    name: str,
    selected_applications: Optional[
        Set[str]
    ] = None,
    selected_explorer_paths: Optional[
        Set[str]
    ] = None,
    selected_vscode_paths: Optional[
        Set[str]
    ] = None,
) -> Path:
    """
    Capture and save a workspace.

    Returns:
        Path: Location of the saved JSON file.
    """

    workspace = capture_workspace(
        name=name,
        selected_applications=(
            selected_applications
        ),
        selected_explorer_paths=(
            selected_explorer_paths
        ),
        selected_vscode_paths=(
            selected_vscode_paths
        ),
    )

    WORKSPACE_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = (
        WORKSPACE_DIRECTORY
        / f"{workspace.name}.json"
    )

    workspace.save(
        file_path
    )

    return file_path


# ============================================================
# List Workspaces
# ============================================================

def list_workspaces() -> List[str]:
    """
    Return all saved workspace names.
    """

    if not WORKSPACE_DIRECTORY.exists():
        return []

    return sorted(
        [
            path.stem
            for path in (
                WORKSPACE_DIRECTORY.glob(
                    "*.json"
                )
            )
        ],
        key=str.lower,
    )


# ============================================================
# Get Workspace
# ============================================================

def get_workspace(
    name: str,
) -> dict:
    """
    Load a workspace JSON file.
    """

    if not name or not name.strip():
        raise ValueError(
            "Workspace name cannot be empty."
        )

    file_path = (
        WORKSPACE_DIRECTORY
        / f"{name.strip()}.json"
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"Workspace not found: {name}"
        )

    try:
        return json.loads(
            file_path.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError as error:
        raise ValueError(
            "Workspace file contains invalid JSON."
        ) from error


# ============================================================
# Delete Workspace
# ============================================================

def delete_workspace(
    name: str,
) -> bool:
    """
    Delete a saved workspace JSON file.

    This does NOT delete the user's actual
    applications, files, folders, or projects.
    """

    if not name or not name.strip():
        raise ValueError(
            "Workspace name cannot be empty."
        )

    file_path = (
        WORKSPACE_DIRECTORY
        / f"{name.strip()}.json"
    )

    if not file_path.exists():
        return False

    file_path.unlink()

    return True