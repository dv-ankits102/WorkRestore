from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


DIALOG_STYLE = """
QDialog {
    background-color: #0b0d12;
    color: #ffffff;
}

QLabel {
    background-color: transparent;
    border: none;
    color: #d7dce8;
}

QLabel#title {
    color: #ffffff;
    font-size: 26px;
    font-weight: 700;
}

QLabel#section {
    color: #ffffff;
    font-size: 17px;
    font-weight: 700;
}

QLabel#version {
    color: #8fa0bd;
    font-size: 14px;
}

QLabel#text {
    color: #b8c0d0;
    font-size: 14px;
}

QPushButton {
    color: #ffffff;
    background-color: #252b38;
    border: 1px solid #343c4d;
    border-radius: 8px;
    padding: 9px 28px;
    min-width: 90px;
}

QPushButton:hover {
    background-color: #303849;
}

QPushButton:pressed {
    background-color: #1d2330;
}
"""


def _create_dialog(
    parent,
    title: str,
    content,
    width: int = 650,
    height: int = 500,
) -> QDialog:
    """Create a dark legal/information dialog."""

    dialog = QDialog(parent)

    dialog.setWindowTitle(title)

    dialog.setMinimumSize(
        width,
        height,
    )

    dialog.setStyleSheet(
        DIALOG_STYLE
    )

    layout = QVBoxLayout(
        dialog
    )

    layout.setContentsMargins(
        28,
        26,
        28,
        24,
    )

    layout.setSpacing(
        14
    )

    title_label = QLabel(
        title
    )

    title_label.setObjectName(
        "title"
    )

    layout.addWidget(
        title_label
    )

    if isinstance(content, list):

        for item in content:

            if item["type"] == "section":

                label = QLabel(
                    item["text"]
                )

                label.setObjectName(
                    "section"
                )

                layout.addWidget(
                    label
                )

            else:

                label = QLabel(
                    item["text"]
                )

                label.setObjectName(
                    "text"
                )

                label.setWordWrap(
                    True
                )

                layout.addWidget(
                    label
                )

    else:

        label = QLabel(
            content
        )

        label.setObjectName(
            "text"
        )

        label.setWordWrap(
            True
        )

        layout.addWidget(
            label
        )

    layout.addStretch()

    button_layout = QHBoxLayout()

    button_layout.addStretch()

    close_button = QPushButton(
        "Close"
    )

    close_button.clicked.connect(
        dialog.accept
    )

    button_layout.addWidget(
        close_button
    )

    layout.addLayout(
        button_layout
    )

    return dialog


def show_about(parent) -> None:
    """Show About WorkRestore dialog."""

    content = [
        {
            "type": "text",
            "text": "Version 1.0.0",
        },
        {
            "type": "text",
            "text": (
                "WorkRestore is a Windows desktop "
                "application designed to save and "
                "restore your working environment."
            ),
        },
        {
            "type": "text",
            "text": (
                "It can remember selected applications, "
                "File Explorer folders and VS Code "
                "workspaces so that you can restore "
                "your workspace when needed."
            ),
        },
        {
            "type": "section",
            "text": "Features",
        },
        {
            "type": "text",
            "text": (
                "• Save workspaces<br>"
                "• Select applications individually<br>"
                "• Save File Explorer folders<br>"
                "• Save VS Code workspaces<br>"
                "• Restore saved workspaces<br>"
                "• Delete saved workspaces<br>"
                "• Local workspace storage"
            ),
        },
        {
            "type": "section",
            "text": "Developer",
        },
        {
            "type": "text",
            "text": (
                "WorkRestore is an independent "
                "software project."
            ),
        },
        {
            "type": "text",
            "text": "© 2026 WorkRestore",
        },
    ]

    dialog = _create_dialog(
        parent,
        "About WorkRestore",
        content,
        650,
        520,
    )

    dialog.exec()


def show_privacy(parent) -> None:
    """Show Privacy Policy dialog."""

    content = [
        {
            "type": "section",
            "text": "Privacy Policy",
        },
        {
            "type": "text",
            "text": (
                "WorkRestore is designed to work locally "
                "on your Windows computer."
            ),
        },
        {
            "type": "text",
            "text": (
                "Saved workspace information is stored "
                "locally and is used only to restore the "
                "workspace selected by you."
            ),
        },
        {
            "type": "section",
            "text": "Local Data",
        },
        {
            "type": "text",
            "text": (
                "Workspace names, application information, "
                "File Explorer paths and VS Code workspace "
                "paths may be stored locally."
            ),
        },
        {
            "type": "section",
            "text": "No Account Required",
        },
        {
            "type": "text",
            "text": (
                "WorkRestore does not require an online "
                "account to save or restore local workspaces."
            ),
        },
    ]

    dialog = _create_dialog(
        parent,
        "Privacy Policy",
        content,
        650,
        500,
    )

    dialog.exec()


def show_terms(parent) -> None:
    """Show Terms & Conditions dialog."""

    content = [
        {
            "type": "section",
            "text": "Terms & Conditions",
        },
        {
            "type": "text",
            "text": (
                "WorkRestore is provided as a desktop "
                "utility for managing and restoring "
                "Windows workspaces."
            ),
        },
        {
            "type": "section",
            "text": "User Responsibility",
        },
        {
            "type": "text",
            "text": (
                "You are responsible for selecting the "
                "applications, folders and workspaces "
                "that WorkRestore should save or restore."
            ),
        },
        {
            "type": "section",
            "text": "System Changes",
        },
        {
            "type": "text",
            "text": (
                "Restoring a workspace may open applications "
                "or folders on your computer. Make sure the "
                "selected workspace information is correct."
            ),
        },
        {
            "type": "section",
            "text": "Use at Your Own Risk",
        },
        {
            "type": "text",
            "text": (
                "WorkRestore is an independent software "
                "project and should be used with reasonable "
                "care on your Windows system."
            ),
        },
    ]

    dialog = _create_dialog(
        parent,
        "Terms & Conditions",
        content,
        650,
        500,
    )

    dialog.exec()


def show_licenses(parent) -> None:
    """Show Open Source Licenses dialog."""

    content = [
        {
            "type": "section",
            "text": "Open Source Licenses",
        },
        {
            "type": "text",
            "text": (
                "WorkRestore uses open-source Python and "
                "PySide6 libraries."
            ),
        },
        {
            "type": "section",
            "text": "PySide6",
        },
        {
            "type": "text",
            "text": (
                "PySide6 provides the Qt-based desktop "
                "user interface used by WorkRestore."
            ),
        },
        {
            "type": "section",
            "text": "psutil",
        },
        {
            "type": "text",
            "text": (
                "psutil is used for accessing running "
                "process information."
            ),
        },
        {
            "type": "section",
            "text": "pywin32",
        },
        {
            "type": "text",
            "text": (
                "pywin32 is used for Windows-specific "
                "functionality such as window and system "
                "integration."
            ),
        },
        {
            "type": "text",
            "text": (
                "Please refer to the respective projects "
                "for their complete license terms."
            ),
        },
    ]

    dialog = _create_dialog(
        parent,
        "Open Source Licenses",
        content,
        650,
        520,
    )

    dialog.exec()