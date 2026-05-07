from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
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

        # Validator AFTER creating widget
        self.age_input.setValidator(QIntValidator(1, 120))

        self.layout.addWidget(self.age_input)

        # HEIGHT
        self.layout.addWidget(QLabel("Height (cm):"))

        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("e.g. 175")

        # Validator AFTER creating widget
        self.height_input.setValidator(
            QDoubleValidator(50.0, 300.0, 2)
        )

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

    def save_profile(self):

        try:
            name = self.name_input.text().strip()

            if not name:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Name is required"
                )
                return

            age = int(self.age_input.text())
            height = float(self.height_input.text())

            if height <= 0:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Height must be greater than zero"
                )
                return

            database.save_user_profile(name, age, height)

            QMessageBox.information(
                self,
                "Success",
                "Profile saved!"
            )

        except ValueError:

            QMessageBox.warning(
                self,
                "Error",
                "Please enter valid values"
            )

    def load_profile(self):

        user = database.get_user_profile()

        if user:

            self.name_input.setText(user[0] or "")
            self.age_input.setText(str(user[1] or ""))
            self.height_input.setText(str(user[2] or ""))