import json
import subprocess
from pathlib import Path
from typing import Dict, List


WORKSPACE_DIRECTORY = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "workspaces"
)


def load_workspace(
    workspace_name: str,
) -> Dict:
    """Load a saved workspace."""

    if not workspace_name.strip():
        raise ValueError(
            "Workspace name cannot be empty."
        )

    file_path = (
        WORKSPACE_DIRECTORY
        / f"{workspace_name}.json"
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"Workspace not found: {workspace_name}"
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


def _restore_applications(
    applications: List[Dict],
) -> List[str]:
    """
    Restore saved applications.

    If document_path is available, open the
    application together with the saved document.
    """

    restored: List[str] = []

    for application in applications:
        name = application.get(
            "name",
            "",
        )

        executable = application.get(
            "executable",
            "",
        )

        document_path = application.get(
            "document_path",
            "",
        )

        if not name or not executable:
            continue

        executable_path = Path(
            executable
        )

        if not executable_path.is_file():
            continue

        # VS Code is restored separately.
        if name.lower() == "code.exe":
            continue

        try:
            # -------------------------------------------------
            # Restore application + exact saved document
            # -------------------------------------------------

            if document_path:
                document = Path(
                    document_path
                )

                if document.is_file():
                    subprocess.Popen(
                        [
                            str(executable_path),
                            str(document),
                        ]
                    )

                    restored.append(
                        f"Application: {name} - "
                        f"{document}"
                    )

                    continue

            # -------------------------------------------------
            # Restore normal application
            # -------------------------------------------------

            subprocess.Popen(
                [
                    str(executable_path)
                ]
            )

            restored.append(
                f"Application: {name}"
            )

        except OSError:
            continue

    return restored


def _restore_vscode(
    vscode_windows: List[Dict],
) -> List[str]:
    """Restore saved VS Code workspaces."""

    restored: List[str] = []

    for vscode in vscode_windows:
        executable = vscode.get(
            "executable",
            "",
        )

        workspace_path = vscode.get(
            "workspace_path",
            "",
        )

        if not executable:
            continue

        if not workspace_path:
            continue

        executable_path = Path(
            executable
        )

        project_path = Path(
            workspace_path
        )

        if not executable_path.is_file():
            continue

        if not project_path.is_dir():
            continue

        try:
            subprocess.Popen(
                [
                    str(executable_path),
                    str(project_path),
                ]
            )

            restored.append(
                f"VS Code: {workspace_path}"
            )

        except OSError:
            continue

    return restored


def _restore_explorer(
    explorer_windows: List[Dict],
) -> List[str]:
    """Restore saved File Explorer folders."""

    restored: List[str] = []

    for explorer in explorer_windows:
        folder_path = explorer.get(
            "path",
            "",
        )

        if not folder_path:
            continue

        path = Path(
            folder_path
        )

        if not path.is_dir():
            continue

        try:
            subprocess.Popen(
                [
                    "explorer.exe",
                    str(path),
                ]
            )

            restored.append(
                f"Explorer: {folder_path}"
            )

        except OSError:
            continue

    return restored


def restore_workspace(
    workspace_name: str,
) -> List[str]:
    """
    Restore exactly what is stored in a workspace.

    Applications with document_path are opened
    together with their saved document.
    """

    workspace = load_workspace(
        workspace_name
    )

    applications = workspace.get(
        "applications",
        [],
    )

    vscode_windows = workspace.get(
        "vscode_windows",
        [],
    )

    explorer_windows = workspace.get(
        "explorer_windows",
        [],
    )

    restored: List[str] = []

    # 1. Applications
    restored.extend(
        _restore_applications(
            applications
        )
    )

    # 2. VS Code
    restored.extend(
        _restore_vscode(
            vscode_windows
        )
    )

    # 3. Explorer
    restored.extend(
        _restore_explorer(
            explorer_windows
        )
    )

    return restored