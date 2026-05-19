from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QFrame,
    QMessageBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

import database


class LoginPage(QWidget):

    def __init__(self, switch_to_main):
        super().__init__()

        self.switch_to_main = switch_to_main
        self.is_register_mode = False

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setObjectName("LoginCard")
        card.setFixedWidth(440)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(36, 36, 36, 36)
        card_layout.setSpacing(0)

        # Brand mark
        brand = QLabel("◈  Smart Finance")
        brand.setStyleSheet(
            "color: #3b82f6; font-size: 15px; font-weight: 700; background: transparent;"
        )
        brand.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(brand)
        card_layout.addSpacing(24)

        self.title = QLabel("Welcome back")
        self.title.setObjectName("PageTitle")
        self.title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.title)

        card_layout.addSpacing(4)

        self.subtitle = QLabel("Sign in to manage your income, expenses, and budget.")
        self.subtitle.setObjectName("Subtitle")
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setWordWrap(True)
        card_layout.addWidget(self.subtitle)

        card_layout.addSpacing(28)

        # Username
        card_layout.addWidget(self._field_label("Username"))
        card_layout.addSpacing(6)
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter your username")
        self.username.setMinimumHeight(42)
        card_layout.addWidget(self.username)

        card_layout.addSpacing(14)

        # Password
        card_layout.addWidget(self._field_label("Password"))
        card_layout.addSpacing(6)
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter your password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setMinimumHeight(42)
        card_layout.addWidget(self.password)

        card_layout.addSpacing(14)

        # Confirm password (register only)
        self.confirm_label = self._field_label("Confirm Password")
        card_layout.addWidget(self.confirm_label)
        card_layout.addSpacing(6)
        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Re-enter your password")
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setMinimumHeight(42)
        card_layout.addWidget(self.confirm_password)

        card_layout.addSpacing(24)

        self.primary_btn = QPushButton("Login")
        self.primary_btn.setMinimumHeight(46)
        self.primary_btn.setCursor(Qt.PointingHandCursor)
        self.primary_btn.clicked.connect(self.submit)
        card_layout.addWidget(self.primary_btn)

        card_layout.addSpacing(16)

        # Switch mode row
        switch_row = QHBoxLayout()
        switch_row.setAlignment(Qt.AlignCenter)

        self.question_label = QLabel("New here?")
        self.question_label.setObjectName("Subtitle")

        self.switch_btn = QPushButton("Create an account")
        self.switch_btn.setObjectName("LinkButton")
        self.switch_btn.setCursor(Qt.PointingHandCursor)
        self.switch_btn.clicked.connect(self.toggle_mode)

        switch_row.addWidget(self.question_label)
        switch_row.addWidget(self.switch_btn)
        card_layout.addLayout(switch_row)

        main_layout.addWidget(card)
        self.update_mode()

    def _field_label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("FieldLabel")
        return lbl

    def toggle_mode(self):
        self.is_register_mode = not self.is_register_mode
        self.update_mode()

    def update_mode(self):
        self.confirm_label.setVisible(self.is_register_mode)
        self.confirm_password.setVisible(self.is_register_mode)

        if self.is_register_mode:
            self.title.setText("Create account")
            self.subtitle.setText("New here? Create an account to start tracking.")
            self.primary_btn.setText("Create Account")
            self.question_label.setText("Already have an account?")
            self.switch_btn.setText("Login")
        else:
            self.title.setText("Welcome back")
            self.subtitle.setText("Sign in to manage your income, expenses, and budget.")
            self.primary_btn.setText("Login")
            self.question_label.setText("New here?")
            self.switch_btn.setText("Create an account")

    def submit(self):
        if self.is_register_mode:
            self.register()
        else:
            self.login()

    def login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill all fields.")
            return

        user = database.login_user(username, password)
        if user:
            self.switch_to_main()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")

    def register(self):
        username         = self.username.text().strip()
        password         = self.password.text().strip()
        confirm_password = self.confirm_password.text().strip()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Error", "Please fill all fields.")
            return
        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return
        if len(password) < 4:
            QMessageBox.warning(self, "Error", "Password must be at least 4 characters.")
            return

        if database.register_user(username, password):
            QMessageBox.information(self, "Success", "Account created. You can log in now.")
            self.password.clear()
            self.confirm_password.clear()
            self.is_register_mode = False
            self.update_mode()
        else:
            QMessageBox.warning(self, "Error", "Username already exists.")
