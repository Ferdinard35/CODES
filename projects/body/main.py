import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,
    QPushButton, QStackedWidget, QFrame, QVBoxLayout
)
from PySide6.QtGui import QFont

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

        self.setWindowTitle("Weight Tracker")
        self.setMinimumSize(900, 600)

        database.init_db()

        # MAIN WIDGET
        central = QWidget()
        self.setCentralWidget(central)
        self.layout = QHBoxLayout(central)

        
        # SIDEBAR
        
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(180)
        self.sidebar_layout = QVBoxLayout(self.sidebar)

        self.buttons = []

        self.btn_dashboard = self.create_btn("Dashboard")
        self.btn_add = self.create_btn("Add Entry")
        self.btn_history = self.create_btn("History")
        self.btn_goals = self.create_btn("Goals")
        self.btn_chart = self.create_btn("Charts")
        self.btn_settings = self.create_btn("Settings")

        self.buttons = [
            self.btn_dashboard,
            self.btn_add,
            self.btn_history,
            self.btn_goals,
            self.btn_chart,
            self.btn_settings
        ]

        for btn in self.buttons:
            self.sidebar_layout.addWidget(btn)

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

        
        # SIGNALS
        
        self.page_add.entry_added.connect(self.full_refresh)

        
        # NAVIGATION
        
        self.btn_dashboard.clicked.connect(lambda: self.switch(0))
        self.btn_add.clicked.connect(lambda: self.switch(1))
        self.btn_history.clicked.connect(lambda: self.switch(2))
        self.btn_goals.clicked.connect(lambda: self.switch(3))
        self.btn_chart.clicked.connect(lambda: self.switch(4))
        self.btn_settings.clicked.connect(lambda: self.switch(5))

        # default page
        self.switch(0)

    
    # BUTTON CREATION
    
    def create_btn(self, text):
        btn = QPushButton(text)
        btn.setFont(QFont("Arial", 10))
        btn.setMinimumHeight(40)
        btn.setCheckable(True)
        return btn

    
    # SIDEBAR ACTIVE STATE 
    
    def set_active(self, active_btn):
        for btn in self.buttons:
            btn.setChecked(False)
        active_btn.setChecked(True)

    
    # PAGE SWITCH
    
    def switch(self, index):

        self.pages.setCurrentIndex(index)

        mapping = {
            0: self.btn_dashboard,
            1: self.btn_add,
            2: self.btn_history,
            3: self.btn_goals,
            4: self.btn_chart,
            5: self.btn_settings
        }

        self.set_active(mapping[index])

        # refresh pages when opened
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

        self.pages.setCurrentIndex(0)
        self.set_active(self.btn_dashboard)



# RUN APP

if __name__ == "__main__":
    app = QApplication(sys.argv)

    apply_styles(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())