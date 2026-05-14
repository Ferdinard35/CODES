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

        
        # WINDOW SETTINGS
        
        self.setWindowTitle("Smart Finance Tracker")
        self.setMinimumSize(1200, 700)

        # Initialize database
        database.create_table()

        
        # CENTRAL WIDGET
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)


        # SIDEBAR
        
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")

        self.sidebar.setFixedWidth(240)

        self.sidebar_layout = QVBoxLayout(self.sidebar)

        self.sidebar_layout.setContentsMargins(15, 20, 15, 20)
        self.sidebar_layout.setSpacing(12)

        
        # APP TITLE
        
        self.logo = QLabel("💰 Smart Finance")

        self.logo.setFont(QFont("Segoe UI", 18, QFont.Bold))

        self.logo.setAlignment(Qt.AlignCenter)

        self.sidebar_layout.addWidget(self.logo)

        
        # NAVIGATION BUTTONS
        
        self.dashboard_btn = self.create_sidebar_button(
            "Dashboard"
        )

        self.add_btn = self.create_sidebar_button(
            "Add Transaction"
        )

        self.history_btn = self.create_sidebar_button(
            "History"
        )

        self.analytics_btn = self.create_sidebar_button(
            "Analytics"
        )

        # ADD BUTTONS TO SIDEBAR
        self.sidebar_layout.addWidget(self.dashboard_btn)

        self.sidebar_layout.addWidget(self.add_btn)

        self.sidebar_layout.addWidget(self.history_btn)

        self.sidebar_layout.addWidget(self.analytics_btn)

        self.sidebar_layout.addStretch()

        
        # STACKED PAGES
        
        self.stack = QStackedWidget()

        self.dashboard_page = Dashboard()

        self.add_transaction_page = AddTransactionPage()

        self.history_page = HistoryPage()

        self.analytics_page = AnalyticsPage()

        # ADD PAGES
        self.stack.addWidget(self.dashboard_page)

        self.stack.addWidget(self.add_transaction_page)

        self.stack.addWidget(self.history_page)

        self.stack.addWidget(self.analytics_page)


        # ADD TO MAIN LAYOUT
        
        self.main_layout.addWidget(self.sidebar)

        self.main_layout.addWidget(self.stack)


        # BUTTON CONNECTIONS
        
        self.dashboard_btn.clicked.connect(
            lambda: self.switch_page(0)
        )

        self.add_btn.clicked.connect(
            lambda: self.switch_page(1)
        )

        self.history_btn.clicked.connect(
            lambda: self.switch_page(2)
        )

        self.analytics_btn.clicked.connect(
            lambda: self.switch_page(3)
        )

       
        # DEFAULT PAGE
     
        self.switch_page(0)

        
        # STYLESHEET
      
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f172a;
            }

            QWidget {
                color: white;
                font-family: Segoe UI;
            }

            #sidebar {
                background-color: #1e293b;
                border-right: 1px solid #334155;
            }

            QPushButton {
                background-color: #334155;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px;
                text-align: left;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #475569;
            }

            QPushButton:pressed {
                background-color: #2563eb;
            }

            QLabel {
                color: white;
            }
        """)

    
    # CREATE SIDEBAR BUTTON

    def create_sidebar_button(self, text):

        button = QPushButton(text)

        button.setCursor(Qt.PointingHandCursor)

        button.setMinimumHeight(48)

        return button

    
    # SWITCH PAGE
    
    def switch_page(self, index):

        self.stack.setCurrentIndex(index)



# RUN APPLICATION

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())