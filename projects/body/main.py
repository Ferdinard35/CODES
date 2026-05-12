import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,
    QPushButton, QStackedWidget, QFrame, QVBoxLayout, QLabel
)

from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from dashboard import Dashboard
from add_entry import AddEntryPage
from history_page import HistoryPage
from settings_page import SettingsPage
from goal_setting import GoalSettingPage
from chart_page import ChartPage

from stylesheet import apply_styles
import database


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fitness Tracker")
        self.setMinimumSize(1200, 750)
        database.init_db()

        # CENTRAL
        central = QWidget()
        self.setCentralWidget(central)
        self.layout = QHBoxLayout(central)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # SIDEBAR
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(240)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(15, 20, 15, 20)
        self.sidebar_layout.setSpacing(8)

        # BRAND
        brand = QLabel("⚡ FitSync")
        brand.setFont(QFont("Segoe UI", 16, QFont.Bold))
        brand.setStyleSheet("color: white; padding: 10px;")
        self.sidebar_layout.addWidget(brand)
        self.sidebar_layout.addSpacing(10)

        # BUTTONS
        self.btn_dashboard = self.create_btn("Dashboard")
        self.btn_add = self.create_btn("Add Entry")
        self.btn_history = self.create_btn("History")
        self.btn_goals = self.create_btn("Goals")
        self.btn_chart = self.create_btn("Analytics")
        self.btn_settings = self.create_btn("Settings")

        self.buttons = [
            self.btn_dashboard,
            self.btn_add,
            self.btn_history,
            self.btn_goals,
            self.btn_chart,
            self.btn_settings
        ]

        for b in self.buttons:
            self.sidebar_layout.addWidget(b)

        self.sidebar_layout.addStretch()
        self.layout.addWidget(self.sidebar)

        # STACKED PAGES
        self.pages = QStackedWidget()
        self.layout.addWidget(self.pages)

        self.page_dashboard = Dashboard()
        self.page_add = AddEntryPage()
        self.page_history = HistoryPage()
        self.page_goals = GoalSettingPage()
        self.page_chart = ChartPage()
        self.page_settings = SettingsPage()

        self.pages.addWidget(self.page_dashboard)
        self.pages.addWidget(self.page_add)
        self.pages.addWidget(self.page_history)
        self.pages.addWidget(self.page_goals)
        self.pages.addWidget(self.page_chart)
        self.pages.addWidget(self.page_settings)

        # 🔥 SIGNALS
        self.page_goals.goal_saved.connect(self.page_dashboard.refresh_dashboard)

        # 👉 NEW: goals update connection
        self.page_goals.goal_saved.connect(self.on_goals_updated)

        self.btn_dashboard.clicked.connect(lambda: self.switch(0))
        self.btn_add.clicked.connect(lambda: self.switch(1))
        self.btn_history.clicked.connect(lambda: self.switch(2))
        self.btn_goals.clicked.connect(lambda: self.switch(3))
        self.btn_chart.clicked.connect(lambda: self.switch(4))
        self.btn_settings.clicked.connect(lambda: self.switch(5))

        self.switch(0)

    # BUTTON CREATION
    def create_btn(self, text):

        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(45)

        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #cbd5e1;
                border: none;
                text-align: left;
                padding: 10px 14px;
                border-radius: 10px;
                font-size: 13px;
            }

            QPushButton:hover {
                background-color: #111827;
                color: white;
                padding-left: 18px;
            }

            QPushButton:checked {
                background-color: #1d4ed8;
                color: white;
                font-weight: bold;
                border-left: 3px solid #3b82f6;
            }
        """)

        return btn

    # PAGE SWITCH
    def switch(self, index):

        self.pages.setCurrentIndex(index)

        for i, btn in enumerate(self.buttons):
            btn.setChecked(i == index)

        if index == 0:
            self.page_dashboard.refresh_dashboard()

        elif index == 2:
            self.page_history.load_data()

        elif index == 4:
            self.page_chart.update_chart()

        elif index == 5:
            self.page_settings.load_profile()

    # GLOBAL REFRESH
    def full_refresh(self):

        self.page_dashboard.refresh_dashboard()
        self.page_history.load_data()
        self.page_chart.update_chart()
        self.switch(0)

    # 🔥 NEW: handle goal updates properly
    def on_goals_updated(self):

        # refresh chart or dashboard if needed
        self.page_chart.update_chart()
        self.page_dashboard.refresh_dashboard()

        # stay on goals page but ensure values reload
        self.page_goals.refresh_goals()

    # RUN APP
if __name__ == "__main__":

    app = QApplication(sys.argv)

    apply_styles(app)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())