from app.services.window_service import (
    get_open_windows,
)


windows = get_open_windows()

for window in windows:
    print(
        f"TITLE: {window.title}"
    )
    print(
        f"PROCESS: {window.process_name}"
    )
    print(
        f"PID: {window.process_id}"
    )
    print(
        f"EXE: {window.executable}"
    )
    print("-" * 60)