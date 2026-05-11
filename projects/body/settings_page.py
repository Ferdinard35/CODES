from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFrame
)

from PySide6.QtGui import (
    QIntValidator,
    QDoubleValidator,
    QFont
)

from PySide6.QtCore import Qt

import database


class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()

       
        # MAIN LAYOUT
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(25)

      
        # TITLE
        self.title = QLabel("⚙ Profile Settings")
        self.title.setFont(
            QFont("Segoe UI", 22, QFont.Bold)
        )
        self.title.setStyleSheet("""
            color: white;
        """)
        self.layout.addWidget(self.title)

        
        # SUBTITLE
        self.subtitle = QLabel(
            "Manage your personal fitness profile information."
        )
        self.subtitle.setStyleSheet("""
            color: #94a3b8;
            font-size: 14px;
        """)
        self.layout.addWidget(self.subtitle)

        
        # CARD
        self.card = QFrame()
        self.card.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border-radius: 22px;
                border: 1px solid #1f2937;
            }
        """)

        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setContentsMargins(30, 30, 30, 30)
        self.card_layout.setSpacing(22)

        
        # INPUTS
        self.name_input = self.create_input(
            "👤 Name",
            "Enter your name"
        )
        self.age_input = self.create_input(
            "🎂 Age",
            "e.g. 21"
        )
        self.age_input.setValidator(
            QIntValidator(1, 120)
        )

        self.height_input = self.create_input(
            "📏 Height (cm)",
            "e.g. 175"
        )

        self.height_input.setValidator(
            QDoubleValidator(50.0, 250.0, 1)
        )

        
        # SAVE BUTTON
        self.save_btn = QPushButton("Save Profile")
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.setMinimumHeight(55)
        self.save_btn.clicked.connect(
            self.save_profile
        )

        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 14px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #4ade80;
            }

            QPushButton:pressed {
                background-color: #16a34a;
            }
        """)

        self.card_layout.addWidget(self.save_btn)
        self.layout.addWidget(self.card)
        self.layout.addStretch()

        # LOAD PROFILE
        self.load_profile()

   
    # CREATE INPUT
   

    def create_input(self, label_text, placeholder):

        container = QVBoxLayout()

        label = QLabel(label_text)

        label.setStyleSheet("""
            color: #e2e8f0;
            font-size: 14px;
            font-weight: 600;
        """)

        field = QLineEdit()

        field.setPlaceholderText(placeholder)

        field.setMinimumHeight(50)

        field.setStyleSheet("""
            QLineEdit {
                background-color: #1e293b;
                color: white;
                border: 2px solid transparent;
                border-radius: 14px;
                padding-left: 15px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 2px solid #2563eb;
                background-color: #243244;
            }
        """)

        container.addWidget(label)

        container.addWidget(field)

        self.card_layout.addLayout(container)

        return field

    
    # SAVE PROFILE
   

    def save_profile(self):

        name = self.name_input.text().strip()

        age_text = self.age_input.text().strip()

        height_text = self.height_input.text().strip()

        if not name:

            QMessageBox.warning(
                self,
                "Error",
                "Name is required"
            )

            return

        try:

            age = int(age_text) if age_text else None

            height = (
                float(height_text)
                if height_text else None
            )

            if age is None or age <= 0:

                QMessageBox.warning(
                    self,
                    "Error",
                    "Valid age required"
                )

                return

            if height is None or height <= 0:

                QMessageBox.warning(
                    self,
                    "Error",
                    "Valid height required"
                )

                return

            database.save_user_profile(
                name,
                age,
                height
            )

            QMessageBox.information(
                self,
                "Success",
                "Profile saved successfully!"
            )

        except ValueError:

            QMessageBox.warning(
                self,
                "Error",
                "Please enter valid numbers"
            )

    
    # LOAD PROFILE
   

    def load_profile(self):

        user = database.get_user_profile()

        if not user:
            return

        name, age, height = user

        self.name_input.setText(name or "")

        self.age_input.setText(
            str(age) if age else ""
        )

        self.height_input.setText(
            str(height) if height else ""
        )