import time

from app.services.restore_service import (
    restore_workspace,
)

from app.services.settings_service import (
    get_last_workspace,
    get_restore_delay,
    is_auto_restore_enabled,
)


def auto_restore_last_workspace() -> list[str]:
    """Automatically restore the last workspace."""

    if not is_auto_restore_enabled():
        return []

    workspace_name = (
        get_last_workspace()
    )

    if not workspace_name:
        return []

    delay = get_restore_delay()

    if delay > 0:
        time.sleep(delay)

    try:
        return restore_workspace(
            workspace_name
        )

    except (
        FileNotFoundError,
        OSError,
        ValueError,
    ):
        return []