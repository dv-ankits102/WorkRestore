from app.services.vscode_process_service import (
    get_vscode_processes,
)


processes = get_vscode_processes()

if not processes:
    print("No VS Code processes found.")

for process in processes:
    print("=" * 70)
    print(f"PID: {process.pid}")
    print(f"NAME: {process.name}")
    print(f"PARENT PID: {process.parent_pid}")
    print(f"EXE: {process.executable}")
    print(f"CWD: {process.working_directory}")

    print("COMMAND LINE:")

    for argument in process.command_line:
        print(f"  {argument}")