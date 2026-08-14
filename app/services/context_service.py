from dataclasses import dataclass
from typing import List

import psutil


@dataclass
class ApplicationContext:
    """Context information for a running application."""

    process_id: int
    name: str
    executable: str
    command_line: List[str]
    working_directory: str


def get_application_contexts() -> List[ApplicationContext]:
    """Collect context information from running applications."""

    contexts: List[ApplicationContext] = []

    for process in psutil.process_iter(
        [
            "pid",
            "name",
            "exe",
            "cmdline",
            "cwd",
        ]
    ):
        try:
            name = process.info["name"]
            executable = process.info["exe"]

            if not name or not executable:
                continue

            command_line = (
                process.info["cmdline"]
                or []
            )

            working_directory = (
                process.info["cwd"]
                or ""
            )

            contexts.append(
                ApplicationContext(
                    process_id=process.info["pid"],
                    name=name,
                    executable=executable,
                    command_line=command_line,
                    working_directory=working_directory,
                )
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    return contexts