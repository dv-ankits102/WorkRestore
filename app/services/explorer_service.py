from dataclasses import dataclass
from typing import List

import win32com.client


@dataclass
class ExplorerWindow:
    """Information about an open File Explorer window."""

    title: str
    path: str


def get_open_explorer_windows() -> List[ExplorerWindow]:
    """Return currently open File Explorer folders."""

    windows: List[ExplorerWindow] = []

    shell = win32com.client.Dispatch(
        "Shell.Application"
    )

    for window in shell.Windows():
        try:
            full_name = str(
                window.FullName
            ).lower()

            if "explorer.exe" not in full_name:
                continue

            path = str(
                window.Document.Folder.Self.Path
            )

            title = str(
                window.Document.Folder.Title
            )

            if not path:
                continue

            windows.append(
                ExplorerWindow(
                    title=title,
                    path=path,
                )
            )

        except Exception:
            continue

    return windows