from dataclasses import dataclass
from typing import List

import psutil


@dataclass
class VSCodeProcessInfo:
    """Information about a VS Code process."""

    pid: int
    name: str
    executable: str
    command_line: List[str]
    working_directory: str
    parent_pid: int | None


def get_vscode_processes() -> List[VSCodeProcessInfo]:
    """Return all VS Code related processes."""

    processes: List[VSCodeProcessInfo] = []

    for process in psutil.process_iter(
        [
            "pid",
            "name",
            "exe",
            "cmdline",
            "cwd",
            "ppid",
        ]
    ):
        try:
            name = process.info["name"]

            if not name:
                continue

            if name.lower() != "code.exe":
                continue

            processes.append(
                VSCodeProcessInfo(
                    pid=process.info["pid"],
                    name=name,
                    executable=process.info["exe"] or "",
                    command_line=(
                        process.info["cmdline"] or []
                    ),
                    working_directory=(
                        process.info["cwd"] or ""
                    ),
                    parent_pid=process.info["ppid"],
                )
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    return processes