from dataclasses import dataclass
from typing import List

import win32gui
import win32process
import psutil


@dataclass
class WindowInfo:
    """Information about a visible application window."""

    title: str
    process_id: int
    process_name: str
    executable: str


def get_open_windows() -> List[WindowInfo]:
    """Return visible application windows."""

    windows: List[WindowInfo] = []

    def window_callback(
        hwnd: int,
        _: int,
    ) -> None:
        if not win32gui.IsWindowVisible(hwnd):
            return

        title = win32gui.GetWindowText(hwnd).strip()

        if not title:
            return

        try:
            _, process_id = win32process.GetWindowThreadProcessId(
                hwnd
            )

            process = psutil.Process(process_id)

            process_name = process.name()
            executable = process.exe()

            windows.append(
                WindowInfo(
                    title=title,
                    process_id=process_id,
                    process_name=process_name,
                    executable=executable,
                )
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            return

    win32gui.EnumWindows(
        window_callback,
        0,
    )

    return windows