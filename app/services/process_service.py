from typing import Dict, List, Set

import psutil
import win32gui
import win32process


# ============================================================
# PROCESSES THAT SHOULD NEVER APPEAR
# ============================================================

IGNORED_PROCESSES = {
    "system",
    "system idle process",
    "registry",

    # Windows
    "smss.exe",
    "csrss.exe",
    "wininit.exe",
    "services.exe",
    "lsass.exe",
    "svchost.exe",
    "fontdrvhost.exe",
    "dwm.exe",
    "winlogon.exe",
    "searchhost.exe",
    "searchindexer.exe",
    "sihost.exe",
    "ctfmon.exe",
    "runtimebroker.exe",
    "applicationframehost.exe",
    "conhost.exe",
    "spoolsv.exe",
    "wudfhost.exe",
    "dllhost.exe",
    "taskhostw.exe",
    "backgroundtaskhost.exe",
    "textinputhost.exe",
    "shellexperiencehost.exe",
    "startmenuexperiencehost.exe",
    "searchapp.exe",
    "widgets.exe",

    # Windows Security
    "securityhealthservice.exe",
    "securityhealthsystray.exe",
    "msmpeng.exe",

    # Windows services
    "microsoftedgeupdate.exe",
    "gamingservices.exe",
    "gamingservicesnet.exe",

    # Common helpers
    "tabtip.exe",
    "sccache.exe",
}


# ============================================================
# USER APPLICATIONS
# ============================================================

KNOWN_USER_APPS = {
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

    # Windows applications
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

    # Python
    "python.exe",
    "pythonw.exe",

    # Communication
    "slack.exe",
    "discord.exe",
    "teams.exe",
    "ms-teams.exe",
    "zoom.exe",
    "telegram.exe",
    "whatsapp.exe",

    # Other applications
    "postman.exe",
    "figma.exe",
    "vlc.exe",
    "spotify.exe",
}


def _get_visible_process_ids() -> Set[int]:
    """
    Return process IDs that own visible top-level windows.
    """

    process_ids: Set[int] = set()

    def callback(
        hwnd: int,
        _: int,
    ) -> None:
        """Collect process IDs for visible windows."""

        try:
            if not win32gui.IsWindowVisible(hwnd):
                return

            title = win32gui.GetWindowText(
                hwnd
            ).strip()

            if not title:
                return

            _, process_id = (
                win32process.GetWindowThreadProcessId(
                    hwnd
                )
            )

            if process_id:
                process_ids.add(
                    process_id
                )

        except Exception:
            return

    win32gui.EnumWindows(
        callback,
        0,
    )

    return process_ids


def _has_visible_window(
    process_id: int,
    visible_process_ids: Set[int],
) -> bool:
    """
    Check whether a process owns a visible window.
    """

    return process_id in visible_process_ids


def _is_known_user_application(
    process_name: str,
) -> bool:
    """
    Return True when the process is a known desktop application.
    """

    return (
        process_name.lower()
        in KNOWN_USER_APPS
    )


def _is_background_process(
    process_name: str,
) -> bool:
    """
    Detect common background/helper processes.
    """

    normalized_name = (
        process_name.lower()
    )

    if normalized_name in IGNORED_PROCESSES:
        return True

    background_suffixes = (
        "helper.exe",
        "background.exe",
        "service.exe",
        "servicehost.exe",
        "updater.exe",
        "update.exe",
    )

    return normalized_name.endswith(
        background_suffixes
    )


def get_running_applications() -> List[str]:
    """
    Return user-facing Windows applications.

    The function combines:
    - visible-window detection
    - known application allow-list
    - background-process filtering

    File Explorer is intentionally excluded because
    Explorer windows are handled by explorer_service.py.
    """

    applications: Dict[str, int] = {}

    visible_process_ids = (
        _get_visible_process_ids()
    )

    for process in psutil.process_iter(
        [
            "pid",
            "name",
        ]
    ):
        try:
            process_id = process.info.get(
                "pid"
            )

            name = process.info.get(
                "name"
            )

            if not process_id or not name:
                continue

            normalized_name = (
                name.lower()
            )

            # ------------------------------------------------
            # Ignore Windows/background processes
            # ------------------------------------------------

            if _is_background_process(
                normalized_name
            ):
                continue

            # ------------------------------------------------
            # Explorer handled separately
            # ------------------------------------------------

            if normalized_name == "explorer.exe":
                continue

            # ------------------------------------------------
            # Known user applications
            # ------------------------------------------------

            if _is_known_user_application(
                normalized_name
            ):

                # Known desktop apps should normally
                # have a visible window.
                if not _has_visible_window(
                    process_id,
                    visible_process_ids,
                ):
                    continue

                applications[
                    name
                ] = process_id

                continue

            # ------------------------------------------------
            # Unknown processes
            #
            # Only accept them when they have a visible
            # top-level window.
            # ------------------------------------------------

            if process_id not in visible_process_ids:
                continue

            # ------------------------------------------------
            # Ignore obvious helper processes
            # ------------------------------------------------

            if (
                normalized_name.endswith(
                    "helper.exe"
                )
                or normalized_name.endswith(
                    "background.exe"
                )
                or normalized_name.endswith(
                    "service.exe"
                )
                or normalized_name.endswith(
                    "servicehost.exe"
                )
            ):
                continue

            applications[
                name
            ] = process_id

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    return sorted(
        applications.keys(),
        key=str.lower,
    )