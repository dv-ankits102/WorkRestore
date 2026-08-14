from app.services.explorer_service import (
    get_open_explorer_windows,
)


windows = get_open_explorer_windows()

if not windows:
    print("No File Explorer windows found.")

for window in windows:
    print(f"TITLE: {window.title}")
    print(f"PATH:  {window.path}")
    print("-" * 60)