from pathlib import Path
import json

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from app.services.workspace_service import (
    WORKSPACE_DIRECTORY,
)


class WorkspaceCard(QFrame):
    """Visual card representing a saved workspace."""

    restore_clicked = Signal(str)
    delete_clicked = Signal(str)

    def __init__(
        self,
        workspace_name: str,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.workspace_name = workspace_name

        self.setObjectName("workspaceCard")

        self._setup_ui()
        self._load_details()

    def _setup_ui(self) -> None:
        """Build the workspace card UI."""

        self.setStyleSheet(
            """
            QFrame#workspaceCard {
                background-color: #171a22;
                border: 1px solid #292e3a;
                border-radius: 12px;
            }

            QFrame#workspaceCard:hover {
                border: 1px solid #4f7cff;
                background-color: #1c2130;
            }

            QLabel#workspaceIcon {
                font-size: 26px;
            }

            QLabel#workspaceName {
                font-size: 16px;
                font-weight: 600;
                color: #ffffff;
            }

            QLabel#workspaceDetails {
                font-size: 12px;
                color: #8b93a7;
            }

            QLabel#workspacePath {
                font-size: 11px;
                color: #687184;
            }

            QPushButton#restoreButton {
                background-color: #4f7cff;
                border: none;
                border-radius: 7px;
                padding: 8px 14px;
                color: white;
                font-weight: 600;
            }

            QPushButton#restoreButton:hover {
                background-color: #638cff;
            }

            QPushButton#deleteButton {
                background-color: transparent;
                border: 1px solid #65323d;
                border-radius: 7px;
                padding: 8px 12px;
                color: #ff9ca9;
            }

            QPushButton#deleteButton:hover {
                background-color: #352126;
            }
            """
        )

        main_layout = QHBoxLayout()

        main_layout.setContentsMargins(
            16,
            14,
            16,
            14,
        )

        main_layout.setSpacing(12)

        # -----------------------------------------------------
        # Icon
        # -----------------------------------------------------

        icon = QLabel("💻")

        icon.setObjectName(
            "workspaceIcon"
        )

        main_layout.addWidget(icon)

        # -----------------------------------------------------
        # Information
        # -----------------------------------------------------

        info_layout = QVBoxLayout()

        info_layout.setSpacing(4)

        name_label = QLabel(
            self.workspace_name
        )

        name_label.setObjectName(
            "workspaceName"
        )

        self.details_label = QLabel(
            "Loading workspace details..."
        )

        self.details_label.setObjectName(
            "workspaceDetails"
        )

        self.path_label = QLabel(
            ""
        )

        self.path_label.setObjectName(
            "workspacePath"
        )

        self.path_label.setWordWrap(
            True
        )

        info_layout.addWidget(
            name_label
        )

        info_layout.addWidget(
            self.details_label
        )

        info_layout.addWidget(
            self.path_label
        )

        main_layout.addLayout(
            info_layout,
            1,
        )

        # -----------------------------------------------------
        # Restore
        # -----------------------------------------------------

        restore_button = QPushButton(
            "Restore"
        )

        restore_button.setObjectName(
            "restoreButton"
        )

        restore_button.clicked.connect(
            self._restore
        )

        main_layout.addWidget(
            restore_button
        )

        # -----------------------------------------------------
        # Delete
        # -----------------------------------------------------

        delete_button = QPushButton(
            "Delete"
        )

        delete_button.setObjectName(
            "deleteButton"
        )

        delete_button.clicked.connect(
            self._delete
        )

        main_layout.addWidget(
            delete_button
        )

        self.setLayout(
            main_layout
        )

    def _load_details(self) -> None:
        """Load workspace information from its JSON file."""

        file_path = (
            WORKSPACE_DIRECTORY
            / f"{self.workspace_name}.json"
        )

        try:
            data = json.loads(
                file_path.read_text(
                    encoding="utf-8"
                )
            )

        except (
            OSError,
            json.JSONDecodeError,
        ):
            self.details_label.setText(
                "Workspace details unavailable"
            )

            return

        applications = data.get(
            "applications",
            [],
        )

        explorer_windows = data.get(
            "explorer_windows",
            [],
        )

        vscode_windows = data.get(
            "vscode_windows",
            [],
        )

        application_count = len(
            applications
        )

        explorer_count = len(
            explorer_windows
        )

        vscode_count = len(
            vscode_windows
        )

        self.details_label.setText(
            (
                f"💻 {application_count} Applications"
                f"   •   "
                f"📁 {explorer_count} Folders"
                f"   •   "
                f"🧑‍💻 {vscode_count} VS Code"
            )
        )

        # -----------------------------------------------------
        # Show VS Code workspace path if available
        # -----------------------------------------------------

        if vscode_windows:
            workspace_paths = []

            for window in vscode_windows:
                path = window.get(
                    "workspace_path"
                )

                if path and path not in workspace_paths:
                    workspace_paths.append(
                        path
                    )

            if workspace_paths:
                self.path_label.setText(
                    "📂 "
                    + "  •  ".join(
                        workspace_paths
                    )
                )

        # -----------------------------------------------------
        # Show application names if available
        # -----------------------------------------------------

        application_names = []

        for application in applications:
            name = application.get(
                "name"
            )

            if name:
                application_names.append(
                    name
                )

        if application_names:
            self.path_label.setText(
                self.path_label.text()
                + (
                    "\n⚙ "
                    + ", ".join(
                        application_names
                    )
                )
            )

    def _restore(self) -> None:
        """Emit restore signal."""

        self.restore_clicked.emit(
            self.workspace_name
        )

    def _delete(self) -> None:
        """Emit delete signal."""

        self.delete_clicked.emit(
            self.workspace_name
        )