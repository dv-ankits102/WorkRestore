from typing import List, Tuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.services.explorer_service import (
    ExplorerWindow,
    get_open_explorer_windows,
)

from app.services.process_service import (
    get_running_applications,
)

from app.services.restore_service import (
    restore_workspace,
)

from app.services.settings_service import (
    set_last_workspace,
)

from app.services.vscode_service import (
    VSCodeWindow,
    get_vscode_windows,
)

from app.services.workspace_service import (
    WORKSPACE_DIRECTORY,
    delete_workspace,
    list_workspaces,
    save_workspace,
)

from app.ui.legal_dialog import (
    show_about,
    show_licenses,
    show_privacy,
    show_terms,
)

from app.ui.styles import APP_STYLE

from app.ui.widgets.status_card import (
    StatusCard,
)

from app.ui.widgets.workspace_card import (
    WorkspaceCard,
)


class MainWindow(QMainWindow):
    """Main WorkRestore dashboard."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("WorkRestore")

        self.setMinimumSize(
            950,
            700,
        )

        self.resize(
            1100,
            800,
        )

        self.setStyleSheet(
            APP_STYLE
            + """
            QMainWindow {
                background-color: #0b0d12;
                color: #ffffff;
            }

            QWidget {
                color: #ffffff;
            }

            QMenuBar {
                background-color: #0b0d12;
                color: #ffffff;
                border: none;
                padding: 4px 6px;
            }

            QMenuBar::item {
                background-color: transparent;
                color: #ffffff;
                padding: 7px 12px;
                border-radius: 6px;
            }

            QMenuBar::item:selected {
                background-color: #252b38;
                color: #ffffff;
            }

            QMenu {
                background-color: #171a22;
                color: #ffffff;
                border: 1px solid #343c4d;
                padding: 6px;
            }

            QMenu::item {
                background-color: transparent;
                color: #ffffff;
                padding: 8px 22px;
                border-radius: 5px;
            }

            QMenu::item:selected {
                background-color: #4f7cff;
                color: #ffffff;
            }

            QMenu::separator {
                height: 1px;
                background-color: #343c4d;
                margin: 5px 8px;
            }

            QDialog {
                background-color: #0b0d12;
                color: #ffffff;
            }

            QDialog QLabel {
                color: #ffffff;
                background-color: transparent;
            }

            QDialog QLineEdit {
                color: #ffffff;
                background-color: #171a22;
                border: 1px solid #343c4d;
            }

            QDialog QTextBrowser,
            QDialog QTextEdit {
                color: #ffffff;
                background-color: #171a22;
                border: 1px solid #343c4d;
            }

            QDialog QPushButton {
                color: #ffffff;
                background-color: #252b38;
                border: 1px solid #343c4d;
            }

            QDialog QPushButton:hover {
                color: #ffffff;
                background-color: #303849;
            }
            """
        )

        self._applications: List[str] = []

        self._explorer_windows: List[
            ExplorerWindow
        ] = []

        self._vscode_windows: List[
            VSCodeWindow
        ] = []

        self._application_checkboxes: List[
            Tuple[str, QCheckBox]
        ] = []

        self._explorer_checkboxes: List[
            Tuple[ExplorerWindow, QCheckBox]
        ] = []

        self._vscode_checkboxes: List[
            Tuple[VSCodeWindow, QCheckBox]
        ] = []

        self._setup_ui()
        self._setup_menu()

        self._refresh_workspace_data()
        self._load_saved_workspaces()

    # =========================================================
    # MENU
    # =========================================================

    def _setup_menu(self) -> None:
        """Create application menu."""

        menu_bar = self.menuBar()

        help_menu = menu_bar.addMenu(
            "Help"
        )

        help_menu.setStyleSheet(
            """
            QMenu {
                background-color: #171a22;
                color: #ffffff;
                border: 1px solid #343c4d;
                padding: 6px;
            }

            QMenu::item {
                color: #ffffff;
                background-color: transparent;
                padding: 8px 22px;
                border-radius: 5px;
            }

            QMenu::item:selected {
                color: #ffffff;
                background-color: #4f7cff;
            }

            QMenu::separator {
                height: 1px;
                background-color: #343c4d;
                margin: 5px 8px;
            }
            """
        )

        about_action = help_menu.addAction(
            "About WorkRestore"
        )

        privacy_action = help_menu.addAction(
            "Privacy Policy"
        )

        terms_action = help_menu.addAction(
            "Terms & Conditions"
        )

        licenses_action = help_menu.addAction(
            "Open Source Licenses"
        )

        help_menu.addSeparator()

        exit_action = help_menu.addAction(
            "Exit"
        )

        about_action.triggered.connect(
            lambda: show_about(self)
        )

        privacy_action.triggered.connect(
            lambda: show_privacy(self)
        )

        terms_action.triggered.connect(
            lambda: show_terms(self)
        )

        licenses_action.triggered.connect(
            lambda: show_licenses(self)
        )

        exit_action.triggered.connect(
            self.close
        )

    # =========================================================
    # MAIN UI
    # =========================================================

    def _setup_ui(self) -> None:
        """Build the main WorkRestore interface."""

        root = QWidget()

        root.setStyleSheet(
            """
            QWidget {
                background-color: #0b0d12;
                color: #ffffff;
            }
            """
        )

        root_layout = QVBoxLayout(root)

        root_layout.setContentsMargins(
            28,
            24,
            28,
            24,
        )

        root_layout.setSpacing(18)

        # =====================================================
        # HEADER
        # =====================================================

        header = QHBoxLayout()

        title_layout = QVBoxLayout()

        title = QLabel(
            "WorkRestore"
        )

        title.setStyleSheet(
            """
            QLabel {
                color: #ffffff;
                font-size: 32px;
                font-weight: 700;
                background: transparent;
                border: none;
            }
            """
        )

        subtitle = QLabel(
            "Save and restore your Windows workspace."
        )

        subtitle.setStyleSheet(
            """
            QLabel {
                color: #8b93a7;
                font-size: 14px;
                background: transparent;
                border: none;
            }
            """
        )

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        header.addLayout(
            title_layout
        )

        header.addStretch()

        status = QLabel(
            "● Ready"
        )

        status.setStyleSheet(
            """
            QLabel {
                color: #72e6a5;
                font-weight: 600;
                padding: 10px 16px;
                background-color: #17271f;
                border: 1px solid #28523c;
                border-radius: 8px;
            }
            """
        )

        header.addWidget(status)

        root_layout.addLayout(header)

        # =====================================================
        # SCROLL
        # =====================================================

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)

        scroll.setFrameShape(
            QFrame.NoFrame
        )

        scroll.setStyleSheet(
            """
            QScrollArea {
                background-color: #0b0d12;
                border: none;
            }

            QScrollArea > QWidget > QWidget {
                background-color: #0b0d12;
            }

            QScrollBar:vertical {
                background-color: #0f1117;
                width: 10px;
                margin: 0;
            }

            QScrollBar::handle:vertical {
                background-color: #343c4d;
                border-radius: 5px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #4f7cff;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
            }
            """
        )

        content = QWidget()

        content.setStyleSheet(
            """
            QWidget {
                background-color: #0b0d12;
            }
            """
        )

        content_layout = QVBoxLayout(
            content
        )

        content_layout.setContentsMargins(
            0,
            5,
            0,
            20,
        )

        content_layout.setSpacing(16)

        current_title = QLabel(
            "CURRENT WORKSPACE"
        )

        current_title.setStyleSheet(
            """
            QLabel {
                color: #ffffff;
                font-size: 16px;
                font-weight: 700;
                background: transparent;
                border: none;
            }
            """
        )

        content_layout.addWidget(
            current_title
        )

        # =====================================================
        # STATUS CARDS
        # =====================================================

        stats_layout = QHBoxLayout()

        stats_layout.setSpacing(12)

        self.apps_status = StatusCard(
            "Applications",
            0,
            "💻",
        )

        self.folders_status = StatusCard(
            "Folders",
            0,
            "📁",
        )

        self.vscode_status = StatusCard(
            "VS Code",
            0,
            "🧑‍💻",
        )

        stats_layout.addWidget(
            self.apps_status
        )

        stats_layout.addWidget(
            self.folders_status
        )

        stats_layout.addWidget(
            self.vscode_status
        )

        content_layout.addLayout(
            stats_layout
        )

        # =====================================================
        # APPLICATIONS
        # =====================================================

        applications_frame = (
            self._create_selection_frame(
                "💻  Applications"
            )
        )

        self.applications_layout = (
            applications_frame.layout()
        )

        if self.applications_layout is None:
            raise RuntimeError(
                "Applications layout was not created."
            )

        content_layout.addWidget(
            applications_frame
        )

        # =====================================================
        # EXPLORER
        # =====================================================

        explorer_frame = (
            self._create_selection_frame(
                "📁  File Explorer"
            )
        )

        self.explorer_layout = (
            explorer_frame.layout()
        )

        if self.explorer_layout is None:
            raise RuntimeError(
                "Explorer layout was not created."
            )

        content_layout.addWidget(
            explorer_frame
        )

        # =====================================================
        # VS CODE
        # =====================================================

        vscode_frame = (
            self._create_selection_frame(
                "🧑‍💻  VS Code Workspaces"
            )
        )

        self.vscode_layout = (
            vscode_frame.layout()
        )

        if self.vscode_layout is None:
            raise RuntimeError(
                "VS Code layout was not created."
            )

        content_layout.addWidget(
            vscode_frame
        )

        # =====================================================
        # SELECT
        # =====================================================

        selection_buttons = QHBoxLayout()

        select_all_button = QPushButton(
            "☑ Select All"
        )

        deselect_all_button = QPushButton(
            "☐ Deselect All"
        )

        select_all_button.clicked.connect(
            self._select_all
        )

        deselect_all_button.clicked.connect(
            self._deselect_all
        )

        selection_buttons.addWidget(
            select_all_button
        )

        selection_buttons.addWidget(
            deselect_all_button
        )

        selection_buttons.addStretch()

        content_layout.addLayout(
            selection_buttons
        )

        # =====================================================
        # REFRESH
        # =====================================================

        self.refresh_button = QPushButton(
            "🔄 Refresh Workspace"
        )

        self.refresh_button.setMinimumHeight(
            42
        )

        self.refresh_button.clicked.connect(
            self._refresh_workspace
        )

        content_layout.addWidget(
            self.refresh_button
        )

        # =====================================================
        # SAVE
        # =====================================================

        self.save_button = QPushButton(
            "+  Save Selected Workspace"
        )

        self.save_button.setObjectName(
            "primaryButton"
        )

        self.save_button.setMinimumHeight(
            48
        )

        self.save_button.clicked.connect(
            self._save_workspace
        )

        content_layout.addWidget(
            self.save_button
        )

        # =====================================================
        # SAVED WORKSPACES
        # =====================================================

        saved_title = QLabel(
            "SAVED WORKSPACES"
        )

        saved_title.setStyleSheet(
            """
            QLabel {
                color: #ffffff;
                font-size: 16px;
                font-weight: 700;
                background: transparent;
                border: none;
            }
            """
        )

        content_layout.addWidget(
            saved_title
        )

        self.workspace_container = QWidget()

        self.workspace_layout = QVBoxLayout(
            self.workspace_container
        )

        self.workspace_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.workspace_layout.setSpacing(
            10
        )

        content_layout.addWidget(
            self.workspace_container
        )

        content_layout.addStretch()

        scroll.setWidget(
            content
        )

        root_layout.addWidget(
            scroll
        )

        self.setCentralWidget(
            root
        )

    # =========================================================
    # SELECTION FRAME
    # =========================================================

    def _create_selection_frame(
        self,
        title_text: str,
    ) -> QFrame:
        """Create selection section."""

        frame = QFrame()

        frame.setStyleSheet(
            """
            QFrame {
                background-color: #171a22;
                border: 1px solid #292e3a;
                border-radius: 12px;
            }
            """
        )

        layout = QVBoxLayout(frame)

        layout.setContentsMargins(
            16,
            14,
            16,
            14,
        )

        layout.setSpacing(8)

        title = QLabel(
            title_text
        )

        title.setStyleSheet(
            """
            QLabel {
                font-size: 15px;
                font-weight: 600;
                color: #ffffff;
                background: transparent;
                border: none;
            }
            """
        )

        layout.addWidget(
            title
        )

        return frame

    # =========================================================
    # REFRESH
    # =========================================================

    def _refresh_workspace(
        self,
    ) -> None:
        """Refresh workspace data."""

        self.refresh_button.setEnabled(
            False
        )

        try:
            self._refresh_workspace_data()

        except Exception as error:
            QMessageBox.critical(
                self,
                "Refresh Failed",
                (
                    "Could not refresh the current "
                    "workspace.\n\n"
                    f"{error}"
                ),
            )

        finally:
            self.refresh_button.setEnabled(
                True
            )

    def _refresh_workspace_data(
        self,
    ) -> None:
        """Read current Windows state."""

        self._applications = (
            get_running_applications()
        )

        self._explorer_windows = (
            get_open_explorer_windows()
        )

        self._vscode_windows = (
            get_vscode_windows()
        )

        self.apps_status.set_value(
            len(self._applications)
        )

        self.folders_status.set_value(
            len(self._explorer_windows)
        )

        self.vscode_status.set_value(
            len(self._vscode_windows)
        )

        self._rebuild_selection_lists()

    # =========================================================
    # CLEAR LAYOUT
    # =========================================================

    def _clear_layout(
        self,
        layout: QVBoxLayout,
    ) -> None:
        """Remove widgets from layout."""

        while layout.count():
            item = layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    # =========================================================
    # CHECKBOX STYLE
    # =========================================================

    def _checkbox_style(self) -> str:
        """Return checkbox stylesheet."""

        return """
            QCheckBox {
                color: #ffffff;
                spacing: 8px;
                padding: 4px;
                background-color: transparent;
                border: none;
            }

            QCheckBox:hover {
                color: #ffffff;
                background-color: #1d2230;
                border-radius: 5px;
            }

            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }

            QCheckBox::indicator:unchecked {
                background-color: #171a22;
                border: 1px solid #596273;
                border-radius: 4px;
            }

            QCheckBox::indicator:checked {
                background-color: #4f7cff;
                border: 1px solid #4f7cff;
                border-radius: 4px;
            }
        """

    # =========================================================
    # REBUILD CHECKBOXES
    # =========================================================

    def _rebuild_selection_lists(
        self,
    ) -> None:
        """Build selection checkboxes."""

        self._clear_layout(
            self.applications_layout
        )

        self._clear_layout(
            self.explorer_layout
        )

        self._clear_layout(
            self.vscode_layout
        )

        self._application_checkboxes.clear()
        self._explorer_checkboxes.clear()
        self._vscode_checkboxes.clear()

        checkbox_style = (
            self._checkbox_style()
        )

        # =====================================================
        # APPLICATIONS
        # =====================================================

        if self._applications:

            for application in self._applications:

                checkbox = QCheckBox(
                    application
                )

                checkbox.setChecked(
                    True
                )

                checkbox.setStyleSheet(
                    checkbox_style
                )

                self.applications_layout.addWidget(
                    checkbox
                )

                self._application_checkboxes.append(
                    (
                        application,
                        checkbox,
                    )
                )

        else:

            label = QLabel(
                "No user applications detected."
            )

            label.setStyleSheet(
                """
                QLabel {
                    color: #8b93a7;
                    padding: 8px;
                    border: none;
                    background: transparent;
                }
                """
            )

            self.applications_layout.addWidget(
                label
            )

        # =====================================================
        # EXPLORER
        # =====================================================

        if self._explorer_windows:

            for explorer in self._explorer_windows:

                checkbox = QCheckBox(
                    f"{explorer.title}  —  "
                    f"{explorer.path}"
                )

                checkbox.setChecked(
                    True
                )

                checkbox.setStyleSheet(
                    checkbox_style
                )

                self.explorer_layout.addWidget(
                    checkbox
                )

                self._explorer_checkboxes.append(
                    (
                        explorer,
                        checkbox,
                    )
                )

        else:

            label = QLabel(
                "No File Explorer folders detected."
            )

            label.setStyleSheet(
                """
                QLabel {
                    color: #8b93a7;
                    padding: 8px;
                    border: none;
                    background: transparent;
                }
                """
            )

            self.explorer_layout.addWidget(
                label
            )

        # =====================================================
        # VS CODE
        # =====================================================

        if self._vscode_windows:

            for vscode in self._vscode_windows:

                workspace_name = (
                    vscode.workspace_name
                    or vscode.title
                )

                label_text = workspace_name

                if vscode.workspace_path:
                    label_text = (
                        f"{label_text}  —  "
                        f"{vscode.workspace_path}"
                    )

                checkbox = QCheckBox(
                    label_text
                )

                checkbox.setChecked(
                    True
                )

                checkbox.setStyleSheet(
                    checkbox_style
                )

                self.vscode_layout.addWidget(
                    checkbox
                )

                self._vscode_checkboxes.append(
                    (
                        vscode,
                        checkbox,
                    )
                )

        else:

            label = QLabel(
                "No VS Code workspaces detected."
            )

            label.setStyleSheet(
                """
                QLabel {
                    color: #8b93a7;
                    padding: 8px;
                    border: none;
                    background: transparent;
                }
                """
            )

            self.vscode_layout.addWidget(
                label
            )

    # =========================================================
    # SELECT ALL
    # =========================================================

    def _select_all(self) -> None:
        """Select every detected item."""

        for _, checkbox in (
            self._application_checkboxes
        ):
            checkbox.setChecked(
                True
            )

        for _, checkbox in (
            self._explorer_checkboxes
        ):
            checkbox.setChecked(
                True
            )

        for _, checkbox in (
            self._vscode_checkboxes
        ):
            checkbox.setChecked(
                True
            )

    # =========================================================
    # DESELECT ALL
    # =========================================================

    def _deselect_all(self) -> None:
        """Deselect every detected item."""

        for _, checkbox in (
            self._application_checkboxes
        ):
            checkbox.setChecked(
                False
            )

        for _, checkbox in (
            self._explorer_checkboxes
        ):
            checkbox.setChecked(
                False
            )

        for _, checkbox in (
            self._vscode_checkboxes
        ):
            checkbox.setChecked(
                False
            )

    # =========================================================
    # SAVE WORKSPACE
    # =========================================================

    def _save_workspace(self) -> None:
        """Save selected workspace."""

        selected_applications = {
            application
            for application, checkbox
            in self._application_checkboxes
            if checkbox.isChecked()
        }

        selected_explorer_paths = {
            explorer.path
            for explorer, checkbox
            in self._explorer_checkboxes
            if checkbox.isChecked()
        }

        selected_vscode_paths = {
            vscode.workspace_path
            for vscode, checkbox
            in self._vscode_checkboxes
            if (
                checkbox.isChecked()
                and vscode.workspace_path
            )
        }

        if not (
            selected_applications
            or selected_explorer_paths
            or selected_vscode_paths
        ):
            QMessageBox.warning(
                self,
                "Nothing Selected",
                (
                    "Please select at least one "
                    "application, folder or VS Code "
                    "workspace."
                ),
            )
            return

        # =====================================================
        # DIALOG
        # =====================================================

        dialog = QDialog(
            self
        )

        dialog.setWindowTitle(
            "Save Workspace"
        )

        dialog.setModal(
            True
        )

        dialog.setFixedWidth(
            500
        )

        dialog.setStyleSheet(
            """
            QDialog {
                background-color: #0b0d12;
                color: #ffffff;
            }

            QLabel {
                color: #ffffff;
                background: transparent;
                border: none;
            }

            QLineEdit {
                color: #ffffff;
                background-color: #171a22;
                border: 1px solid #3d4658;
                border-radius: 8px;
                padding: 11px 12px;
                font-size: 14px;
                selection-background-color: #4f7cff;
                selection-color: #ffffff;
            }

            QLineEdit:focus {
                border: 1px solid #4f7cff;
                background-color: #1b1f29;
            }

            QPushButton {
                color: #ffffff;
                background-color: #252b38;
                border: 1px solid #343c4d;
                border-radius: 8px;
                padding: 9px 22px;
                min-width: 90px;
            }

            QPushButton:hover {
                background-color: #303849;
            }

            QPushButton#saveButton {
                color: #ffffff;
                background-color: #4f7cff;
                border: 1px solid #4f7cff;
                font-weight: 600;
            }

            QPushButton#saveButton:hover {
                background-color: #668cff;
            }
            """
        )

        dialog_layout = QVBoxLayout(
            dialog
        )

        dialog_layout.setContentsMargins(
            24,
            24,
            24,
            24,
        )

        dialog_layout.setSpacing(
            14
        )

        title = QLabel(
            "Save Workspace"
        )

        title.setStyleSheet(
            """
            QLabel {
                font-size: 20px;
                font-weight: 700;
            }
            """
        )

        subtitle = QLabel(
            "Enter a name for your saved workspace."
        )

        subtitle.setStyleSheet(
            """
            QLabel {
                color: #8b93a7;
                font-size: 13px;
            }
            """
        )

        input_box = QLineEdit()

        input_box.setPlaceholderText(
            "e.g. Work, Development, Office"
        )

        input_box.setMinimumHeight(
            42
        )

        input_box.setText("")

        buttons = QDialogButtonBox()

        cancel_button = buttons.addButton(
            "Cancel",
            QDialogButtonBox.RejectRole,
        )

        save_button = buttons.addButton(
            "Save",
            QDialogButtonBox.AcceptRole,
        )

        save_button.setObjectName(
            "saveButton"
        )

        # -----------------------------------------------------
        # IMPORTANT:
        # Do NOT accept dialog before validating input.
        # -----------------------------------------------------

        def save_from_dialog() -> None:
            """Validate name and close dialog."""

            name = input_box.text().strip()

            if not name:
                QMessageBox.warning(
                    dialog,
                    "Invalid Workspace Name",
                    "Please enter a workspace name.",
                )
                input_box.setFocus()
                return

            invalid_characters = (
                '<>:"/\\|?*'
            )

            if any(
                character in name
                for character in invalid_characters
            ):
                QMessageBox.warning(
                    dialog,
                    "Invalid Workspace Name",
                    (
                        "Workspace name contains invalid "
                        "Windows filename characters.\n\n"
                        'Not allowed: < > : " / \\ | ? *'
                    ),
                )
                input_box.setFocus()
                return

            dialog.accept()

        cancel_button.clicked.connect(
            dialog.reject
        )

        save_button.clicked.connect(
            save_from_dialog
        )

        input_box.returnPressed.connect(
            save_from_dialog
        )

        dialog_layout.addWidget(
            title
        )

        dialog_layout.addWidget(
            subtitle
        )

        dialog_layout.addSpacing(
            4
        )

        dialog_layout.addWidget(
            input_box
        )

        dialog_layout.addSpacing(
            8
        )

        dialog_layout.addWidget(
            buttons
        )

        input_box.setFocus()

        # =====================================================
        # SHOW DIALOG
        # =====================================================

        if dialog.exec() != QDialog.Accepted:
            return

        workspace_name = (
            input_box.text().strip()
        )

        # =====================================================
        # FINAL VALIDATION
        # =====================================================

        if not workspace_name:
            QMessageBox.warning(
                self,
                "Invalid Workspace Name",
                "Please enter a workspace name.",
            )
            return

        invalid_characters = (
            '<>:"/\\|?*'
        )

        if any(
            character in workspace_name
            for character in invalid_characters
        ):
            QMessageBox.warning(
                self,
                "Invalid Workspace Name",
                (
                    "Workspace name contains invalid "
                    "Windows filename characters."
                ),
            )
            return

        # =====================================================
        # EXISTING WORKSPACE
        # =====================================================

        existing_file = (
            WORKSPACE_DIRECTORY
            / f"{workspace_name}.json"
        )

        if existing_file.exists():

            answer = QMessageBox.question(
                self,
                "Workspace Already Exists",
                (
                    f"'{workspace_name}' already exists.\n\n"
                    "Do you want to replace it?"
                ),
                QMessageBox.Yes
                | QMessageBox.No,
                QMessageBox.No,
            )

            if answer != QMessageBox.Yes:
                return

        # =====================================================
        # SAVE
        # =====================================================

        self.save_button.setEnabled(
            False
        )

        try:

            file_path = save_workspace(
                name=workspace_name,
                selected_applications=(
                    selected_applications
                ),
                selected_explorer_paths=(
                    selected_explorer_paths
                ),
                selected_vscode_paths=(
                    selected_vscode_paths
                ),
            )

            set_last_workspace(
                workspace_name
            )

            # Refresh workspace cards.
            self._load_saved_workspaces()

            QMessageBox.information(
                self,
                "Workspace Saved",
                (
                    "Workspace saved successfully.\n\n"
                    f"Name: {workspace_name}\n"
                    f"Applications: "
                    f"{len(selected_applications)}\n"
                    f"Folders: "
                    f"{len(selected_explorer_paths)}\n"
                    f"VS Code: "
                    f"{len(selected_vscode_paths)}\n\n"
                    f"File:\n{file_path}"
                ),
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Save Failed",
                (
                    "Could not save workspace.\n\n"
                    f"{type(error).__name__}: "
                    f"{error}"
                ),
            )

        finally:

            self.save_button.setEnabled(
                True
            )

    # =========================================================
    # SAVED WORKSPACES
    # =========================================================

    def _clear_workspace_cards(
        self,
    ) -> None:
        """Remove saved workspace cards."""

        while self.workspace_layout.count():

            item = (
                self.workspace_layout.takeAt(
                    0
                )
            )

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def _load_saved_workspaces(
        self,
    ) -> None:
        """Load saved workspace cards."""

        self._clear_workspace_cards()

        try:

            workspaces = (
                list_workspaces()
            )

        except Exception as error:

            error_label = QLabel(
                (
                    "Could not load workspaces:\n"
                    f"{error}"
                )
            )

            error_label.setStyleSheet(
                """
                QLabel {
                    color: #ff7b86;
                    padding: 20px;
                    border: none;
                    background: transparent;
                }
                """
            )

            self.workspace_layout.addWidget(
                error_label
            )

            return

        if not workspaces:

            empty = QLabel(
                "No saved workspaces yet.\n"
                "Select items above and save your first workspace."
            )

            empty.setAlignment(
                Qt.AlignCenter
            )

            empty.setStyleSheet(
                """
                QLabel {
                    color: #8b93a7;
                    padding: 30px;
                    border: none;
                    background: transparent;
                }
                """
            )

            self.workspace_layout.addWidget(
                empty
            )

            return

        for workspace_name in workspaces:

            card = WorkspaceCard(
                workspace_name
            )

            card.restore_clicked.connect(
                self._restore_workspace
            )

            card.delete_clicked.connect(
                self._delete_workspace
            )

            self.workspace_layout.addWidget(
                card
            )

    # =========================================================
    # RESTORE
    # =========================================================

    def _restore_workspace(
        self,
        workspace_name: str,
    ) -> None:
        """Restore saved workspace."""

        try:

            set_last_workspace(
                workspace_name
            )

            result = restore_workspace(
                workspace_name
            )

            if result is False:

                QMessageBox.warning(
                    self,
                    "Restore Workspace",
                    (
                        "No applications, folders or "
                        "VS Code workspaces could be restored."
                    ),
                )

                return

            QMessageBox.information(
                self,
                "Workspace Restored",
                (
                    f"'{workspace_name}' "
                    "restored successfully."
                ),
            )

        except FileNotFoundError as error:

            QMessageBox.warning(
                self,
                "Workspace Not Found",
                str(error),
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Restore Failed",
                (
                    "Could not restore workspace.\n\n"
                    f"{type(error).__name__}: "
                    f"{error}"
                ),
            )

    # =========================================================
    # DELETE
    # =========================================================

    def _delete_workspace(
        self,
        workspace_name: str,
    ) -> None:
        """Delete saved workspace."""

        answer = QMessageBox.question(
            self,
            "Delete Workspace",
            (
                f"Delete '{workspace_name}'?\n\n"
                "This will only remove the saved workspace."
            ),
            QMessageBox.Yes
            | QMessageBox.No,
            QMessageBox.No,
        )

        if answer != QMessageBox.Yes:
            return

        try:

            deleted = delete_workspace(
                workspace_name
            )

            if not deleted:

                QMessageBox.warning(
                    self,
                    "Workspace Not Found",
                    (
                        f"'{workspace_name}' "
                        "was not found."
                    ),
                )

                return

            self._load_saved_workspaces()

            QMessageBox.information(
                self,
                "Workspace Deleted",
                (
                    f"'{workspace_name}' "
                    "deleted successfully."
                ),
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Delete Failed",
                (
                    "Could not delete workspace.\n\n"
                    f"{type(error).__name__}: "
                    f"{error}"
                ),
            )