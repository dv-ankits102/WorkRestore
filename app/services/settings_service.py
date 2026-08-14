import json
from pathlib import Path
from typing import Optional


SETTINGS_DIRECTORY = (
    Path(__file__).resolve().parents[2]
    / "data"
)

SETTINGS_FILE = (
    SETTINGS_DIRECTORY
    / "settings.json"
)


DEFAULT_SETTINGS = {
    "auto_restore": False,
    "last_workspace": "",
    "restore_delay": 10,
}


def _ensure_settings_file() -> None:
    """Create settings file if it does not exist."""

    SETTINGS_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not SETTINGS_FILE.exists():
        SETTINGS_FILE.write_text(
            json.dumps(
                DEFAULT_SETTINGS,
                indent=4,
            ),
            encoding="utf-8",
        )


def load_settings() -> dict:
    """Load WorkRestore settings."""

    _ensure_settings_file()

    try:
        data = json.loads(
            SETTINGS_FILE.read_text(
                encoding="utf-8"
            )
        )

    except (
        json.JSONDecodeError,
        OSError,
    ):
        return DEFAULT_SETTINGS.copy()

    settings = DEFAULT_SETTINGS.copy()
    settings.update(data)

    return settings


def save_settings(
    settings: dict,
) -> None:
    """Save WorkRestore settings."""

    _ensure_settings_file()

    SETTINGS_FILE.write_text(
        json.dumps(
            settings,
            indent=4,
        ),
        encoding="utf-8",
    )


def set_last_workspace(
    workspace_name: str,
) -> None:
    """Save the last selected workspace."""

    settings = load_settings()

    settings["last_workspace"] = (
        workspace_name.strip()
    )

    save_settings(settings)


def get_last_workspace() -> Optional[str]:
    """Return the last saved workspace."""

    settings = load_settings()

    workspace_name = settings.get(
        "last_workspace",
        "",
    )

    if not workspace_name:
        return None

    return str(workspace_name)


def set_auto_restore(
    enabled: bool,
) -> None:
    """Enable or disable automatic restore."""

    settings = load_settings()

    settings["auto_restore"] = bool(
        enabled
    )

    save_settings(settings)


def is_auto_restore_enabled() -> bool:
    """Return automatic restore state."""

    settings = load_settings()

    return bool(
        settings.get(
            "auto_restore",
            False,
        )
    )


def set_restore_delay(
    seconds: int,
) -> None:
    """Set automatic restore delay."""

    if seconds < 0:
        seconds = 0

    settings = load_settings()

    settings["restore_delay"] = int(
        seconds
    )

    save_settings(settings)


def get_restore_delay() -> int:
    """Return automatic restore delay."""

    settings = load_settings()

    return int(
        settings.get(
            "restore_delay",
            10,
        )
    )