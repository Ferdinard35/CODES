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
    QLabel
)

from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from dashboard import Dashboard
from add_transaction import AddTransactionPage
from history_page import HistoryPage
from analytics_page import AnalyticsPage

import database


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart Finance Tracker")
        self.setMinimumSize(1200, 700)

        # Ensure DB is ready
        database.create_table()

        # CENTRAL WIDGET
        
        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.main_layout = QHBoxLayout(self.central)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

    
        # SIDEBAR
        
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(220)
        self.sidebar.setObjectName("sidebar")

        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(15, 20, 15, 20)
        self.sidebar_layout.setSpacing(12)

        # App Title
        title = QLabel("💰 Finance")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        self.sidebar_layout.addWidget(title)

        # Buttons
        self.btn_dashboard = self.create_button("Dashboard")
        self.btn_add = self.create_button("Add Transaction")
        self.btn_history = self.create_button("History")
        self.btn_analytics = self.create_button("Analytics")

        self.sidebar_layout.addWidget(self.btn_dashboard)
        self.sidebar_layout.addWidget(self.btn_add)
        self.sidebar_layout.addWidget(self.btn_history)
        self.sidebar_layout.addWidget(self.btn_analytics)

        self.sidebar_layout.addStretch()

        
        # STACKED PAGES
        
        self.stack = QStackedWidget()

        self.dashboard_page = Dashboard()
        self.add_page = AddTransactionPage()
        self.history_page = HistoryPage()
        self.analytics_page = AnalyticsPage()

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.add_page)
        self.stack.addWidget(self.history_page)
        self.stack.addWidget(self.analytics_page)

        
        # ADD TO LAYOUT
        
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.stack)

        # BUTTON ACTIONS
       
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0))
        self.btn_add.clicked.connect(lambda: self.switch_page(1))
        self.btn_history.clicked.connect(lambda: self.switch_page(2))
        self.btn_analytics.clicked.connect(lambda: self.switch_page(3))

        
        # STYLES
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f172a;
            }

            #sidebar {
                background-color: #1e293b;
            }

            QPushButton {
                background-color: #334155;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 10px;
                text-align: left;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #475569;
            }

            QPushButton:pressed {
                background-color: #2563eb;
            }
        """)

    
    # CREATE SIDEBAR BUTTON
    def create_button(self, text):

        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(45)

        return btn

    
    # SWITCH PAGES
    
    def switch_page(self, index):
        self.stack.setCurrentIndex(index)


# RUN APP
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
 
    sys.exit(app.exec())