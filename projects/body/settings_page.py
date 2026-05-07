from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import database


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_input)

        self.layout.addWidget(QLabel("Age:"))
        self.age_input = QLineEdit()
        self.layout.addWidget(self.age_input)

        self.layout.addWidget(QLabel("Height (cm):"))
        self.height_input = QLineEdit()
        self.layout.addWidget(self.height_input)

        self.save_btn = QPushButton("Save Profile")
        self.save_btn.clicked.connect(self.save_profile)
        self.layout.addWidget(self.save_btn)

        self.load_profile()

    def save_profile(self):
        try:
            name = self.name_input.text()
            age = int(self.age_input.text())
            height = float(self.height_input.text())

            database.save_user_profile(name, age, height)
            QMessageBox.information(self, "Success", "Profile saved!")

        except:
            QMessageBox.warning(self, "Error", "Invalid input")

    def load_profile(self):
        user = database.get_user_profile()
        if user:
            self.name_input.setText(user[0])
            self.age_input.setText(str(user[1]))
            self.height_input.setText(str(user[2]))