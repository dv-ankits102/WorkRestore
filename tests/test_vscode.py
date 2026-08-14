from app.services.vscode_service import (
    get_vscode_windows,
)


windows = get_vscode_windows()

if not windows:
    print("No visible VS Code windows found.")

for window in windows:
    print("=" * 70)
    print(f"TITLE: {window.title}")
    print(f"WORKSPACE: {window.workspace_name}")
    print(f"PATH: {window.workspace_path}")
    print(f"PID: {window.process_id}")
    print(f"EXE: {window.executable}")