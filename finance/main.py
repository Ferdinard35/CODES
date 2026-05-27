import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QPushButton,
    QStackedWidget, QFrame, QLabel
)
from PySide6.QtCore import Qt

from dashboard          import Dashboard
from add_transaction    import AddTransactionPage
from history_page       import HistoryPage
from analytics_page     import AnalyticsPage
from monthly_report_page import MonthlyReportPage
from settings_page      import SettingsPage
from budget_page        import BudgetPage
from currency_page      import CurrencyPage
from insights_page      import InsightsPage
from login_page         import LoginPage

import database
from theme_manager        import ThemeManager
from user_data_migration  import migrate_to_per_user


class MainWindow(QMainWindow):

    def __init__(self, logout_callback=None):
        super().__init__()

        if not database.is_authenticated():
            raise PermissionError("Authentication required")

        self.logout_callback = logout_callback
        self.setWindowTitle("Smart Finance Tracker")
        self.setMinimumSize(1200, 720)

        database.create_table()
        migrate_to_per_user()          # ← per-user data migration

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── SIDEBAR ──
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(220)

        sb = QVBoxLayout(self.sidebar)
        sb.setContentsMargins(14, 24, 14, 20)
        sb.setSpacing(2)

        # Brand
        brand_row = QHBoxLayout()
        brand_row.setContentsMargins(8, 0, 8, 0)
        b_icon = QLabel("◈")
        b_icon.setStyleSheet("color:#3b82f6;font-size:18px;background:transparent;")
        b_name = QLabel("Smart Finance")
        b_name.setObjectName("SidebarBrand")
        brand_row.addWidget(b_icon)
        brand_row.addWidget(b_name)
        brand_row.addStretch()
        sb.addLayout(brand_row)

        divider = QFrame()
        divider.setObjectName("SidebarDivider")
        divider.setFixedHeight(1)
        sb.addSpacing(16)
        sb.addWidget(divider)
        sb.addSpacing(12)

        # ── PAGES ──
        self.stack = QStackedWidget()

        nav = [
            ("Dashboard",       "⊞",  Dashboard()),
            ("Add Transaction", "+",  AddTransactionPage()),
            ("History",         "◷",  HistoryPage()),
            ("Analytics",       "⋮",  AnalyticsPage()),
            ("Monthly Report",  "≡",  MonthlyReportPage()),
            ("Currency",        "₵",  CurrencyPage()),
            ("Insights",        "✦",  InsightsPage()),
            ("Settings",        "⚙",  SettingsPage(self, self.logout)),
            ("Budget",          "◎",  BudgetPage()),
        ]

        self.pages  = nav
        self.buttons = []

        for idx, (name, icon, page) in enumerate(nav):
            btn = self._nav_btn(name, icon)
            btn.clicked.connect(lambda _, i=idx: self.switch_page(i))
            sb.addWidget(btn)
            self.stack.addWidget(page)
            self.buttons.append(btn)

        sb.addStretch()

        user = database.get_logged_in_user()
        uname = user["username"] if user else ""
        user_lbl = QLabel(f"● {uname}")
        user_lbl.setStyleSheet(
            "color:#64748b;font-size:12px;background:transparent;padding:6px 10px;"
        )
        sb.addWidget(user_lbl)

        root.addWidget(self.sidebar)
        root.addWidget(self.stack)

        self.switch_page(0)

    def _nav_btn(self, text, icon=""):
        btn = QPushButton(f"  {icon}  {text}" if icon else text)
        btn.setObjectName("SidebarButton")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(42)
        return btn

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
    login  = None

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
