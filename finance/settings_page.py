from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QHBoxLayout
)

from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from theme_manager import ThemeManager
import database


class SettingsPage(QWidget):

    def __init__(self, app):
        super().__init__()

        self.app = app

        
        # MAIN LAYOUT
    
        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.main_layout.setSpacing(20)

        
        # TITLE
        
        self.title = QLabel("Settings")
        self.title.setFont(QFont("Segoe UI", 24, QFont.Bold))

        self.main_layout.addWidget(self.title)


        # SETTINGS CARD
        
        self.card = QFrame()
        self.card.setObjectName("settingsCard")

        self.card_layout = QVBoxLayout(self.card)

        self.card_layout.setContentsMargins(20, 20, 20, 20)
        self.card_layout.setSpacing(20)

        
        # THEME SECTION
        
        self.theme_layout = QHBoxLayout()

        self.theme_label = QLabel("Application Theme")
        self.theme_label.setFont(QFont("Segoe UI", 14))

        self.theme_btn = QPushButton()

        self.theme_btn.setMinimumHeight(45)
        self.theme_btn.setCursor(Qt.PointingHandCursor)

        self.theme_btn.clicked.connect(self.toggle_theme)

        self.theme_layout.addWidget(self.theme_label)
        self.theme_layout.addStretch()
        self.theme_layout.addWidget(self.theme_btn)

        self.card_layout.addLayout(self.theme_layout)


        # APP INFO
        
        self.info = QLabel(
            "Smart Finance Tracker\nVersion 1.0"
        )

        self.info.setFont(QFont("Segoe UI", 12))

        self.card_layout.addWidget(self.info)

        self.main_layout.addWidget(self.card)

        self.main_layout.addStretch()

        
        # INITIALIZE UI

        self.update_theme_button()

        
        # STYLES
        
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: white;
                font-family: Segoe UI;
            }

            QLabel {
                color: white;
            }

            #settingsCard {
                background-color: #1e293b;
                border-radius: 18px;
            }

            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 18px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #3b82f6;
            }

            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)


    # TOGGLE THEME
    
    def toggle_theme(self):

        current = database.get_setting(
            "theme",
            ThemeManager.DARK
        )

        if current == ThemeManager.DARK:
            new_theme = ThemeManager.LIGHT
        else:
            new_theme = ThemeManager.DARK

        ThemeManager.apply_theme(
            self.app,
            new_theme
        )

        self.update_theme_button()

    
    # UPDATE BUTTON TEXT
    
    def update_theme_button(self):

        current = database.get_setting(
            "theme",
            ThemeManager.DARK
        )

        if current == ThemeManager.DARK:
            self.theme_btn.setText("Switch to Light Mode ☀")
        else:
            self.theme_btn.setText("Switch to Dark Mode 🌙")