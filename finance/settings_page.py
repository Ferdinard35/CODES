from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QFont

from theme_manager import ThemeManager
import database


class SettingsPage(QWidget):

    def __init__(self, app):
        super().__init__()

        self.app = app

        self.layout = QVBoxLayout(self)

        self.title = QLabel("Settings")
        self.title.setFont(QFont("Segoe UI", 22, QFont.Bold))

        self.layout.addWidget(self.title)

        self.theme_btn = QPushButton("Toggle Theme")
        self.theme_btn.setStyleSheet("""
            background-color: #3b82f6;
            padding: 12px;
            border-radius: 8px;
            font-weight: bold;
        """)

        self.theme_btn.clicked.connect(self.toggle_theme)

        self.layout.addWidget(self.theme_btn)

    def toggle_theme(self):

        current = database.get_setting("theme", "dark")

        new_theme = (
            ThemeManager.LIGHT
            if current == ThemeManager.DARK
            else ThemeManager.DARK
        )

        ThemeManager.apply_theme(self.app, new_theme)