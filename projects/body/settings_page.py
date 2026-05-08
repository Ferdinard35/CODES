from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)

from PySide6.QtGui import QIntValidator, QDoubleValidator
import database


class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # NAME
        self.layout.addWidget(QLabel("Name:"))

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        self.layout.addWidget(self.name_input)

        # AGE
        self.layout.addWidget(QLabel("Age:"))

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("e.g. 21")
        self.age_input.setValidator(QIntValidator(1, 120))
        self.layout.addWidget(self.age_input)

        # HEIGHT
        self.layout.addWidget(QLabel("Height (cm):"))

        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("e.g. 175")
        self.height_input.setValidator(QDoubleValidator(50.0, 250.0, 1))
        self.layout.addWidget(self.height_input)

        # SAVE BUTTON
        self.save_btn = QPushButton("Save Profile")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #219150;
            }
        """)

        self.save_btn.clicked.connect(self.save_profile)
        self.layout.addWidget(self.save_btn)

        self.load_profile()

    
    # SAVE PROFILE 
    
    def save_profile(self):

        name = self.name_input.text().strip()
        age_text = self.age_input.text().strip()
        height_text = self.height_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Error", "Name is required")
            return

        try:
            age = int(age_text) if age_text else None
            height = float(height_text) if height_text else None

            if age is None or age <= 0:
                QMessageBox.warning(self, "Error", "Valid age required")
                return

            if height is None or height <= 0:
                QMessageBox.warning(self, "Error", "Valid height required")
                return

            database.save_user_profile(name, age, height)

            QMessageBox.information(self, "Success", "Profile saved successfully!")

        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid numbers")

    
    # LOAD PROFILE
    
    def load_profile(self):

        user = database.get_user_profile()

        if not user:
            return

        name, age, height = user

        self.name_input.setText(name or "")
        self.age_input.setText(str(age) if age else "")
        self.height_input.setText(str(height) if height else "")