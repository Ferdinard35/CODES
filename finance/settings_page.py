from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QComboBox, QMessageBox, QSizePolicy, QScrollArea
)
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

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        container = QWidget()
        main = QVBoxLayout(container)
        main.setContentsMargins(36, 36, 36, 36)
        main.setSpacing(16)

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

        # TITLE
        title = QLabel("Settings")
        title.setObjectName("PageTitle")
        main.addWidget(title)

        subtitle = QLabel("Manage appearance, data export, and application preferences.")
        subtitle.setObjectName("Subtitle")
        main.addWidget(subtitle)

        main.addSpacing(4)

        # ── PREFERENCES ──
        pref_card = self._make_card("Preferences")
        pref_inner = pref_card.layout()

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.setMinimumHeight(40)
        self.theme_combo.setFixedWidth(180)
        self.theme_combo.currentTextChanged.connect(self.change_theme)

        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["GHS", "USD", "EUR", "GBP"])
        self.currency_combo.setMinimumHeight(40)
        self.currency_combo.setFixedWidth(180)
        self.currency_combo.currentTextChanged.connect(self.change_currency)

        pref_inner.addWidget(self._row(
            "Application Theme", "Choose how the interface looks.", self.theme_combo
        ))
        pref_inner.addWidget(self._row(
            "Currency Label", "Used for display and export preferences.", self.currency_combo
        ))
        main.addWidget(pref_card)

        # ── DATA MANAGEMENT ──
        data_card = self._make_card("Data Management")
        data_inner = data_card.layout()

        self.export_btn = QPushButton("Export Transactions")
        self.export_btn.setObjectName("SecondaryButton")
        self.export_btn.setMinimumHeight(40)
        self.export_btn.setFixedWidth(200)
        self.export_btn.setCursor(Qt.PointingHandCursor)
        self.export_btn.clicked.connect(self.export_data)

        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.setObjectName("DangerButton")
        self.clear_btn.setMinimumHeight(40)
        self.clear_btn.setFixedWidth(120)
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear_data)

        self.transaction_count = QLabel("")
        self.transaction_count.setObjectName("Subtitle")

        data_inner.addWidget(self._row(
            "CSV Backup", "Download a copy of your transaction history.", self.export_btn
        ))
        data_inner.addWidget(self._row(
            "Transaction Records", "Remove all transaction rows after confirmation.", self.clear_btn
        ))
        # Count row
        count_row = QHBoxLayout()
        count_row.setContentsMargins(0, 4, 0, 0)
        count_row.addWidget(self.transaction_count)
        count_row.addStretch()
        data_inner.addLayout(count_row)

        main.addWidget(data_card)

        # ── ACCOUNT ──
        account_card = self._make_card("Account")
        account_inner = account_card.layout()

        self.user_label = QLabel("")
        self.user_label.setObjectName("Subtitle")

        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setObjectName("DangerButton")
        self.logout_btn.setMinimumHeight(40)
        self.logout_btn.setFixedWidth(120)
        self.logout_btn.setCursor(Qt.PointingHandCursor)
        self.logout_btn.clicked.connect(self.logout)

        account_inner.addWidget(self._row(
            "Logged in as", "Manage your session.",
            self.logout_btn, value_widget=self.user_label
        ))
        main.addWidget(account_card)

        # ── APP INFO ──
        info_card = self._make_card("Application")
        info = QLabel(
            f"Smart Finance Tracker  ·  Version 1.0\n"
            f"Database: {database.DB_NAME}"
        )
        info.setObjectName("Subtitle")
        info.setWordWrap(True)
        info_card.layout().addWidget(info)
        main.addWidget(info_card)

        main.addStretch()

        self.load_settings()
        self.refresh_user()
        self.refresh_counts()
        refresh_manager.data_changed.connect(self.refresh_counts)

    # ── CARD FACTORY ──
    def _make_card(self, title_text):
        card = QFrame()
        card.setObjectName("SettingsCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 22, 28, 22)
        layout.setSpacing(0)

        title = QLabel(title_text)
        title.setObjectName("SectionTitle")
        layout.addWidget(title)
        layout.addSpacing(14)
        return card

    # ── ROW FACTORY ──
    def _row(self, label_text, hint_text, control, value_widget=None):
        row_frame = QFrame()
        row_frame.setObjectName("SettingRow")

        row_layout = QHBoxLayout(row_frame)
        row_layout.setContentsMargins(0, 14, 0, 14)
        row_layout.setSpacing(20)

        # Left side: label + optional value + hint
        left = QVBoxLayout()
        left.setSpacing(3)

        lbl = QLabel(label_text)
        lbl.setObjectName("FieldLabel")
        left.addWidget(lbl)

        if value_widget:
            left.addWidget(value_widget)

        hint = QLabel(hint_text)
        hint.setObjectName("Subtitle")
        hint.setWordWrap(True)
        left.addWidget(hint)

        row_layout.addLayout(left, stretch=1)
        row_layout.addWidget(control, alignment=Qt.AlignVCenter | Qt.AlignRight)
        return row_frame

    # ── LOGIC ──
    def load_settings(self):
        theme    = database.get_setting("theme", ThemeManager.DARK)
        currency = database.get_setting("currency", "GHS")

        self.theme_combo.blockSignals(True)
        self.currency_combo.blockSignals(True)
        self.theme_combo.setCurrentText("Light" if theme == ThemeManager.LIGHT else "Dark")
        self.currency_combo.setCurrentText(currency)
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
        self.transaction_count.setText(f"{count} transaction record(s) stored")

    def refresh_user(self):
        user = database.get_logged_in_user()
        self.user_label.setText(user["username"] if user else "Not authenticated")

    def logout(self):
        reply = QMessageBox.question(
            self, "Logout", "Log out and lock the app?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes and self.logout_callback:
            self.logout_callback()
