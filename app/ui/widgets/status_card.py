from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class StatusCard(QFrame):
    """Small dashboard card displaying a workspace statistic."""

    def __init__(
        self,
        title: str,
        value: int = 0,
        icon: str = "●",
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName(
            "statusCard"
        )

        self.setStyleSheet(
            """
            QFrame#statusCard {
                background-color: #171a22;
                border: 1px solid #292e3a;
                border-radius: 12px;
            }

            QLabel#statusIcon {
                font-size: 22px;
            }

            QLabel#statusValue {
                font-size: 24px;
                font-weight: 700;
                color: #ffffff;
            }

            QLabel#statusTitle {
                font-size: 12px;
                color: #8b93a7;
            }
            """
        )

        self._setup_ui(
            title,
            value,
            icon,
        )

    def _setup_ui(
        self,
        title: str,
        value: int,
        icon: str,
    ) -> None:
        """Build the status card."""

        layout = QVBoxLayout()

        layout.setContentsMargins(
            16,
            14,
            16,
            14,
        )

        icon_label = QLabel(
            icon
        )

        icon_label.setObjectName(
            "statusIcon"
        )

        value_label = QLabel(
            str(value)
        )

        value_label.setObjectName(
            "statusValue"
        )

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "statusTitle"
        )

        layout.addWidget(
            icon_label
        )

        layout.addWidget(
            value_label
        )

        layout.addWidget(
            title_label
        )

        self.setLayout(
            layout
        )

        self._value_label = (
            value_label
        )

    def set_value(
        self,
        value: int,
    ) -> None:
        """Update the displayed value."""

        self._value_label.setText(
            str(value)
        )