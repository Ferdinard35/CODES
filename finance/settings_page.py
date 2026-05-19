from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QComboBox,
    QMessageBox,
    QSizePolicy,
    QScrollArea
)

from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from theme_manager import ThemeManager
from export_utils import export_transactions_to_csv
from refresh import refresh_manager
import database


class SettingsPage(QWidget):

    def __init__(self, app, logout_callback=None):
        super().__init__()

        self.app = app
        self.logout_callback = logout_callback

        outer = QVBoxLayout(self)
        outer.setContentsMargins(36, 36, 36, 36)
        outer.setSpacing(6)

        # TITLE
        title = QLabel("Settings")
        title.setObjectName("PageTitle")
        outer.addWidget(title)

        subtitle = QLabel("Manage appearance, data export, and application preferences.")
        subtitle.setObjectName("Subtitle")
        outer.addWidget(subtitle)

        outer.addSpacing(16)

        # PREFERENCES CARD 
        pref_card = self._section_card("Preferences")

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.setMinimumHeight(38)
        self.theme_combo.setFixedWidth(160)
        self.theme_combo.currentTextChanged.connect(self.change_theme)

        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["GHS", "USD", "EUR", "GBP"])
        self.currency_combo.setMinimumHeight(38)
        self.currency_combo.setFixedWidth(160)
        self.currency_combo.currentTextChanged.connect(self.change_currency)

        self._add_row(pref_card, "Application Theme",
                      "Choose how the interface looks.", self.theme_combo)
        self._add_row(pref_card, "Currency Label",
                      "Used for display and export preferences.", self.currency_combo)

        outer.addWidget(pref_card)

        # DATA MANAGEMENT CARD 
        data_card = self._section_card("Data Management")

        self.export_btn = QPushButton("Export Transactions")
        self.export_btn.setObjectName("SecondaryButton")
        self.export_btn.setMinimumHeight(38)
        self.export_btn.setFixedWidth(190)
        self.export_btn.setCursor(Qt.PointingHandCursor)
        self.export_btn.clicked.connect(self.export_data)

        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.setObjectName("DangerButton")
        self.clear_btn.setMinimumHeight(38)
        self.clear_btn.setFixedWidth(120)
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear_data)

        self.transaction_count = QLabel("")
        self.transaction_count.setObjectName("Subtitle")

        self._add_row(data_card, "CSV Backup",
                      "Download a copy of your transaction history.", self.export_btn)
        self._add_row(data_card, "Transaction Records",
                      "Remove all transaction rows after confirmation.", self.clear_btn)
        data_card.layout().addWidget(self.transaction_count)

        outer.addWidget(data_card)

        # ACCOUNT CARD
        account_card = self._section_card("Account")

        self.user_label = QLabel("")
        self.user_label.setObjectName("Subtitle")

        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setObjectName("DangerButton")
        self.logout_btn.setMinimumHeight(38)
        self.logout_btn.setFixedWidth(110)
        self.logout_btn.setCursor(Qt.PointingHandCursor)
        self.logout_btn.clicked.connect(self.logout)

        self._add_row(account_card, "Logged in as",
                      "Manage your session.", self.logout_btn,
                      left_value_widget=self.user_label)

        outer.addWidget(account_card)

        #  APP INFO CARD 
        info_card = self._section_card("Application")
        info = QLabel(
            f"Smart Finance Tracker  ·  Version 1.0\n"
            f"Database: {database.DB_NAME}"
        )
        info.setObjectName("Subtitle")
        info.setWordWrap(True)
        info_card.layout().addWidget(info)

        outer.addWidget(info_card)
        outer.addStretch()

        self.load_settings()
        self.refresh_user()
        self.refresh_counts()
        refresh_manager.data_changed.connect(self.refresh_counts)

    # HELPERS 
    def _section_card(self, title):
        card = QFrame()
        card.setObjectName("SettingsCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(0)

        title_lbl = QLabel(title)
        title_lbl.setObjectName("SectionTitle")
        layout.addWidget(title_lbl)
        layout.addSpacing(16)

        return card

    def _add_row(self, card, title, description, control, left_value_widget=None):
        row_frame = QFrame()
        row_frame.setObjectName("SettingRow")

        row = QHBoxLayout(row_frame)
        row.setContentsMargins(0, 14, 0, 14)
        row.setSpacing(16)

        # Left: text
        text_col = QVBoxLayout()
        text_col.setSpacing(3)

        t = QLabel(title)
        t.setObjectName("FieldLabel")

        d = QLabel(description)
        d.setObjectName("Subtitle")
        d.setWordWrap(True)

        text_col.addWidget(t)
        if left_value_widget:
            text_col.addWidget(left_value_widget)
        text_col.addWidget(d)

        row.addLayout(text_col, stretch=1)
        row.addWidget(control, alignment=Qt.AlignVCenter)

        card.layout().addWidget(row_frame)

    # HELPERS
    def load_settings(self):
        current_theme    = database.get_setting("theme", ThemeManager.DARK)
        current_currency = database.get_setting("currency", "GHS")

        self.theme_combo.blockSignals(True)
        self.currency_combo.blockSignals(True)

        self.theme_combo.setCurrentText("Light" if current_theme == ThemeManager.LIGHT else "Dark")
        self.currency_combo.setCurrentText(current_currency)

        self.theme_combo.blockSignals(False)
        self.currency_combo.blockSignals(False)

    def change_theme(self, value):
        new_theme = ThemeManager.LIGHT if value == "Light" else ThemeManager.DARK
        ThemeManager.apply_theme(self.app, new_theme)
        if hasattr(self.app, "refresh_theme_views"):
            self.app.refresh_theme_views()

    def change_currency(self, value):
        database.set_setting("currency", value)

    def export_data(self):
        filename = export_transactions_to_csv()
        QMessageBox.information(self, "Export Complete", f"Data exported:\n{filename}")

    def clear_data(self):
        count = database.get_transaction_count()
        if count == 0:
            QMessageBox.information(self, "No Data", "There are no transactions to clear.")
            return
        reply = QMessageBox.question(
            self, "Clear Transactions",
            f"This will permanently delete {count} record(s). Continue?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            database.clear_transactions()
            self.refresh_counts()
            QMessageBox.information(self, "Cleared", "All transactions removed.")

    def refresh_counts(self):
        count = database.get_transaction_count()
        self.transaction_count.setText(f"  {count} transaction record(s) stored")

    def refresh_user(self):
        user = database.get_logged_in_user()
        username = user["username"] if user else "Not authenticated"
        self.user_label.setText(username)

    def logout(self):
        reply = QMessageBox.question(
            self, "Logout", "Log out and lock the app?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes and self.logout_callback:
            self.logout_callback()
