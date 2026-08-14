"""
WorkRestore application stylesheet.
"""

APP_STYLE = """
QMainWindow {
    background-color: #0f1117;
}

QWidget {
    font-family: "Segoe UI";
    color: #e6e9ef;
    font-size: 14px;
}

QLabel {
    color: #e6e9ef;
}

QLabel#appTitle {
    font-size: 30px;
    font-weight: 700;
    color: #ffffff;
}

QLabel#appSubtitle {
    font-size: 14px;
    color: #8b93a7;
}

QLabel#sectionTitle {
    font-size: 17px;
    font-weight: 600;
    color: #ffffff;
    margin-top: 8px;
}

QLabel#statNumber {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
}

QLabel#statLabel {
    font-size: 12px;
    color: #8b93a7;
}

QPushButton {
    background-color: #242936;
    border: 1px solid #343a49;
    border-radius: 8px;
    padding: 10px 16px;
    color: #ffffff;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #303746;
}

QPushButton:pressed {
    background-color: #1c2029;
}

QPushButton#primaryButton {
    background-color: #4f7cff;
    border: none;
    color: #ffffff;
}

QPushButton#primaryButton:hover {
    background-color: #638cff;
}

QPushButton#dangerButton {
    background-color: #352126;
    border: 1px solid #65323d;
    color: #ff9ca9;
}

QPushButton#dangerButton:hover {
    background-color: #472730;
}

QListWidget {
    background-color: #171a22;
    border: 1px solid #292e3a;
    border-radius: 10px;
    padding: 6px;
    outline: none;
}

QListWidget::item {
    background-color: #1b1f29;
    border: 1px solid #292e3a;
    border-radius: 8px;
    padding: 12px;
    margin: 4px;
}

QListWidget::item:hover {
    background-color: #222735;
}

QListWidget::item:selected {
    background-color: #263657;
    border: 1px solid #4f7cff;
}

QCheckBox {
    color: #dfe3eb;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
}

QSpinBox {
    background-color: #171a22;
    border: 1px solid #343a49;
    border-radius: 7px;
    padding: 8px;
    color: #ffffff;
}

QSpinBox:focus {
    border: 1px solid #4f7cff;
}

QScrollBar:vertical {
    background-color: #11141a;
    width: 10px;
    margin: 2px;
}

QScrollBar::handle:vertical {
    background-color: #343a49;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #4a5263;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QMessageBox {
    background-color: #171a22;
}

QInputDialog {
    background-color: #171a22;
}
"""