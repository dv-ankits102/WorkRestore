from app.services.context_service import (
    get_application_contexts,
)


contexts = get_application_contexts()

for context in contexts:
    name = context.name.lower()

    if (
        "code" in name
        or "terminal" in name
        or "powershell" in name
        or "cmd" in name
    ):
        print("=" * 60)
        print(f"PID: {context.process_id}")
        print(f"NAME: {context.name}")
        print(f"EXE: {context.executable}")
        print(
            f"CWD: {context.working_directory}"
        )
        print(
            f"CMD: {context.command_line}"
        )