from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QProgressBar,
    QMessageBox
)

from PySide6.QtGui import QFont
from datetime import datetime

import database


class BudgetPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        # TITLE
        self.title = QLabel("Budget Tracking")
        self.title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.layout.addWidget(self.title)

        # INPUT
        self.budget_input = QLineEdit()
        self.budget_input.setPlaceholderText("Enter monthly budget (GHS)")

        self.save_btn = QPushButton("Save Budget")
        self.save_btn.clicked.connect(self.save_budget)

        self.layout.addWidget(self.budget_input)
        self.layout.addWidget(self.save_btn)

        # PROGRESS BAR
        self.progress = QProgressBar()
        self.progress.setMaximum(100)

        self.layout.addWidget(self.progress)

        # STATUS
        self.status = QLabel("")
        self.layout.addWidget(self.status)

        self.load_budget()

    
    # SAVE BUDGET
    
    def save_budget(self):

        try:
            amount = float(self.budget_input.text())
        except:
            QMessageBox.warning(self, "Error", "Invalid amount")
            return

        month = datetime.now().strftime("%Y-%m")

        database.set_budget(month, amount)

        QMessageBox.information(self, "Saved", "Budget updated")

        self.load_budget()


    # LOAD & CALCULATE

    def load_budget(self):

        month = datetime.now().strftime("%Y-%m")

        budget_cents = database.get_budget(month)
        spent_cents = database.get_month_expenses(month)

        budget = budget_cents / 100
        spent = spent_cents / 100

        if budget > 0:
            percent = int((spent / budget) * 100)
        else:
            percent = 0

        self.progress.setValue(min(percent, 100))

        # STATUS TEXT
        if percent > 100:
            self.status.setText("You exceeded your budget!")
            self.status.setStyleSheet("color:red;")
        else:
            remaining = budget - spent
            self.status.setText(f"Remaining: GHS {remaining:,.2f}")
            self.status.setStyleSheet("color:lightgreen;")