import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QStackedWidget, QFrame
)
from PySide6.QtGui import QFont

# Import pages
from dashboard import Dashboard
from add_entry import AddEntryPage
from history_page import HistoryPage
from settings_page import SettingsPage
from goal_setting import GoalSettingPage
from chart_page import ChartPage
import database


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Body Transformation Tracker")
        self.setMinimumSize(800, 600)

        # Init DB
        database.init_db()

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(180)
        self.sidebar.setStyleSheet("background-color: #2C3E50; border-radius: 10px;")
        self.sidebar_layout = QVBoxLayout(self.sidebar)

        self.btn_dashboard = self.create_nav_btn("Dashboard")
        self.btn_add = self.create_nav_btn("Add Entry")
        self.btn_history = self.create_nav_btn("History")
        self.btn_goal_setting = self.create_nav_btn("Set Goals")
        self.btn_chart = self.create_nav_btn("Charts")
        self.btn_settings = self.create_nav_btn("Settings")

        self.sidebar_layout.addWidget(self.btn_dashboard)
        self.sidebar_layout.addWidget(self.btn_add)
        self.sidebar_layout.addWidget(self.btn_history)
        self.sidebar_layout.addWidget(self.btn_goal_setting)
        self.sidebar_layout.addWidget(self.btn_chart)
        self.sidebar_layout.addStretch()
        self.sidebar_layout.addWidget(self.btn_settings)

        self.layout.addWidget(self.sidebar)

        # Pages
        self.pages = QStackedWidget()
        self.layout.addWidget(self.pages)

        self.page_dashboard = Dashboard()
        self.page_add = AddEntryPage()
        self.page_history = HistoryPage()
        self.page_settings = SettingsPage()
        self.page_goal_setting = GoalSettingPage()
        self.page_chart = ChartPage()

        # Add pages
        self.pages.addWidget(self.page_dashboard)   # index 0
        self.pages.addWidget(self.page_add)         # index 1
        self.pages.addWidget(self.page_history)     # index 2
        self.pages.addWidget(self.page_settings)    # index 3
        self.pages.addWidget(self.page_goal_setting)# index 4
        self.pages.addWidget(self.page_chart)       # index 5

        #  CONNECT SIGNAL
        self.page_add.entry_added.connect(self.handle_entry_added)

        # Navigation
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0))
        self.btn_add.clicked.connect(lambda: self.switch_page(1))
        self.btn_history.clicked.connect(lambda: self.switch_page(2))
        self.btn_settings.clicked.connect(lambda: self.switch_page(3))
        self.btn_goal_setting.clicked.connect(lambda: self.switch_page(4))
        self.btn_chart.clicked.connect(lambda: self.switch_page(5))

    def create_nav_btn(self, text):
        btn = QPushButton(text)
        btn.setFont(QFont("Arial", 11, QFont.Bold))
        btn.setMinimumHeight(40)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                text-align: left;
                padding-left: 10px;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
        """)
        return btn

    def handle_entry_added(self):
        #  refresh + go to dashboard
        self.page_dashboard.refresh_dashboard()
        self.pages.setCurrentIndex(0)

    def switch_page(self, index):
        if index == 0:
            self.page_dashboard.refresh_dashboard()
        elif index == 2:
            self.page_history.load_data()
        elif index == 4:
            self.page_goal_setting.refresh_goals()

        self.pages.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
    /* Main Window Background - A deep Navy/Slate instead of pure black */
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                    stop:0 #2c3e50, stop:1 #000000);
    }

    /* The Table Design */
    QTableWidget {
        background-color: rgba(255, 255, 255, 15); /* Semi-transparent white */
        alternate-background-color: rgba(255, 255, 255, 5);
        color: #ffffff;
        gridline-color: #3498db;
        border: 2px solid #3498db;
        border-radius: 10px;
        font-size: 14px;
        selection-background-color: #e74c3c; /* Bright red/orange when you click a row */
    }

    /* Table Headers - Electric Blue */
    QHeaderView::section {
        background-color: #3498db;
        color: white;
        padding: 8px;
        font-weight: bold;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        border: 1px solid #2980b9;
    }

    /* Buttons - Gradient from Blue to Purple */
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                    stop:0 #3498db, stop:1 #9b59b6);
        color: white;
        border-radius: 15px;
        padding: 10px;
        font-weight: bold;
        min-width: 80px;
    }
    
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                    stop:0 #2980b9, stop:1 #8e44ad);
    }

    /* Labels / Text */
    QLabel {
        color: #ecf0f1;
        font-size: 16px;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Entry Inputs */
    QLineEdit {
        background-color: #ffffff;
        color: #2c3e50;
        border: 2px solid #3498db;
        border-radius: 5px;
        padding: 5px;
    }
""")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())