from pathlib import Path
import subprocess
import sys


TASK_NAME = "WorkRestore"


def get_project_root() -> Path:
    """Return the WorkRestore project root."""

    return Path(__file__).resolve().parents[2]


def get_python_executable() -> Path:
    """Return the current Python executable."""

    return Path(sys.executable).resolve()


def get_startup_script() -> Path:
    """Return the automatic restore script."""

    return (
        get_project_root()
        / "startup_restore.py"
    )


def is_startup_enabled() -> bool:
    """Check whether the startup task exists."""

    result = subprocess.run(
        [
            "schtasks",
            "/Query",
            "/TN",
            TASK_NAME,
        ],
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )

    return result.returncode == 0


def enable_startup() -> bool:
    """Create the WorkRestore Windows startup task."""

    python_executable = (
        get_python_executable()
    )

    startup_script = get_startup_script()

    if not python_executable.exists():
        return False

    if not startup_script.exists():
        return False

    task_command = (
        f'"{python_executable}" '
        f'"{startup_script}"'
    )

    result = subprocess.run(
        [
            "schtasks",
            "/Create",
            "/TN",
            TASK_NAME,
            "/TR",
            task_command,
            "/SC",
            "ONLOGON",
            "/F",
        ],
        cwd=str(get_project_root()),
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )

    return result.returncode == 0


def disable_startup() -> bool:
    """Remove the WorkRestore startup task."""

    result = subprocess.run(
        [
            "schtasks",
            "/Delete",
            "/TN",
            TASK_NAME,
            "/F",
        ],
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )

    return result.returncode == 0


def toggle_startup(
    enabled: bool,
) -> bool:
    """Enable or disable Windows startup."""

    if enabled:
        return enable_startup()

    return disable_startup()