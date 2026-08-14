from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import psutil
import win32gui
import win32process


@dataclass
class VSCodeWindow:
    """Information about a VS Code window."""

    hwnd: int
    title: str
    process_id: int
    executable: str
    workspace_name: str
    workspace_path: str


def _extract_workspace_name(
    title: str,
) -> str:
    """Extract workspace name from VS Code window title."""

    suffixes = [
        " - Visual Studio Code",
        " - Code",
    ]

    clean_title = title.strip()

    for suffix in suffixes:
        if suffix in clean_title:
            clean_title = clean_title.split(
                suffix,
                1,
            )[0].strip()

    # Remove common file name prefix.
    if " - " in clean_title:
        parts = clean_title.split(" - ")
        return parts[-1].strip()

    return clean_title


def _find_workspace_path(
    workspace_name: str,
) -> Optional[str]:
    """Find workspace folder in common user directories."""

    home = Path.home()

    search_roots = [
        home / "Desktop",
        home / "Documents",
        home / "Downloads",
        home / "Projects",
        home / "source",
        home / "dev",
    ]

    for root in search_roots:
        if not root.exists():
            continue

        direct_path = root / workspace_name

        if direct_path.is_dir():
            return str(direct_path)

    return None


def get_vscode_windows() -> List[VSCodeWindow]:
    """Return visible VS Code windows."""

    windows: List[VSCodeWindow] = []

    def callback(hwnd: int, _: int) -> None:
        if not win32gui.IsWindowVisible(hwnd):
            return

        title = win32gui.GetWindowText(hwnd).strip()

        if not title:
            return

        try:
            _, process_id = (
                win32process.GetWindowThreadProcessId(
                    hwnd
                )
            )

            process = psutil.Process(process_id)

            if process.name().lower() != "code.exe":
                return

            executable = process.exe()

            workspace_name = (
                _extract_workspace_name(title)
            )

            workspace_path = (
                _find_workspace_path(
                    workspace_name
                )
                or ""
            )

            windows.append(
                VSCodeWindow(
                    hwnd=hwnd,
                    title=title,
                    process_id=process_id,
                    executable=executable,
                    workspace_name=workspace_name,
                    workspace_path=workspace_path,
                )
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            return

    win32gui.EnumWindows(
        callback,
        0,
    )

    return windows