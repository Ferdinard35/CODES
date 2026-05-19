import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QStackedWidget,
    QFrame,
    QLabel,
    QSpacerItem,
    QSizePolicy
)

from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from dashboard import Dashboard
from add_transaction import AddTransactionPage
from history_page import HistoryPage
from analytics_page import AnalyticsPage
from monthly_report_page import MonthlyReportPage
from settings_page import SettingsPage
from budget_page import BudgetPage
from login_page import LoginPage

import database
from theme_manager import ThemeManager


class MainWindow(QMainWindow):

    def __init__(self, logout_callback=None):
        super().__init__()

        if not database.is_authenticated():
            raise PermissionError("Authentication required")

        self.logout_callback = logout_callback
        self.current_user = database.get_logged_in_user()

        self.setWindowTitle("Smart Finance Tracker")
        self.setMinimumSize(1200, 720)

        database.create_table()

        # CENTRAL WIDGET
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # ── SIDEBAR ──
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(220)

        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(14, 24, 14, 20)
        self.sidebar_layout.setSpacing(2)

        # Brand
        brand_row = QHBoxLayout()
        brand_row.setContentsMargins(8, 0, 8, 0)
        brand_icon = QLabel("◈")
        brand_icon.setStyleSheet("color: #3b82f6; font-size: 18px; background: transparent;")
        brand_name = QLabel("Smart Finance")
        brand_name.setObjectName("SidebarBrand")
        brand_row.addWidget(brand_icon)
        brand_row.addWidget(brand_name)
        brand_row.addStretch()
        self.sidebar_layout.addLayout(brand_row)

        # Divider
        divider = QFrame()
        divider.setObjectName("SidebarDivider")
        divider.setFixedHeight(1)
        self.sidebar_layout.addSpacing(16)
        self.sidebar_layout.addWidget(divider)
        self.sidebar_layout.addSpacing(12)

        # STACKED PAGES
        self.stack = QStackedWidget()

        # (label, icon_char, page)
        self.pages = [
            ("Dashboard",       "⊞", Dashboard()),
            ("Add Transaction", "+", AddTransactionPage()),
            ("History",         "◷", HistoryPage()),
            ("Analytics",       "⋮", AnalyticsPage()),
            ("Monthly Report",  "≡", MonthlyReportPage()),
            ("Settings",        "⚙", SettingsPage(self, self.logout)),
            ("Budget",          "◎", BudgetPage()),
        ]

        self.buttons = []

        for index, (name, icon, page) in enumerate(self.pages):
            btn = self.create_sidebar_button(name, icon)
            btn.clicked.connect(lambda checked, i=index: self.switch_page(i))
            self.sidebar_layout.addWidget(btn)
            self.stack.addWidget(page)
            self.buttons.append(btn)

        self.sidebar_layout.addStretch()

        # Logged-in user label at bottom
        user = database.get_logged_in_user()
        username = user["username"] if user else ""
        self.user_label = QLabel(f"● {username}")
        self.user_label.setStyleSheet(
            "color: #64748b; font-size: 12px; background: transparent; padding: 6px 10px;"
        )
        self.sidebar_layout.addWidget(self.user_label)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.stack)

        self.switch_page(0)

    def create_sidebar_button(self, text, icon=""):
        label = f"  {icon}  {text}" if icon else text
        button = QPushButton(label)
        button.setObjectName("SidebarButton")
        button.setCursor(Qt.PointingHandCursor)
        button.setMinimumHeight(42)
        return button

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.buttons):
            btn.setProperty("active", i == index)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def refresh_theme_views(self):
        for _, _, page in self.pages:
            if hasattr(page, "refresh_theme"):
                page.refresh_theme()

    def logout(self):
        database.logout_user()
        self.close()
        if self.logout_callback:
            self.logout_callback()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    saved_theme = database.get_setting("theme", ThemeManager.DARK)
    ThemeManager.apply_theme(app, saved_theme, save=False)

    window = None
    login = None

    def start_main():
        global window, login
        if not database.is_authenticated():
            show_login()
            return
        if login:
            login.close()
            login = None
        window = MainWindow(show_login)
        window.show()

    def show_login():
        global login, window
        if window:
            window.close()
            window = None
        login = LoginPage(start_main)
        login.show()

    if database.is_authenticated():
        start_main()
    else:
        show_login()

    sys.exit(app.exec())
