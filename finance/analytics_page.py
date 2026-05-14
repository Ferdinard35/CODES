from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QHBoxLayout
)

from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas
)

from matplotlib.figure import Figure

import database


class AnalyticsPage(QWidget):

    def __init__(self):
        super().__init__()

        
        # MAIN LAYOUT
        
        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.main_layout.setSpacing(25)

        
        # TITLE

        self.title = QLabel("Financial Analytics")
        self.title.setFont(QFont("Segoe UI", 24, QFont.Bold))

        self.main_layout.addWidget(self.title)

        
        # TOP STATS LAYOUT
        
        self.stats_layout = QHBoxLayout()
        self.stats_layout.setSpacing(20)

        
        # TOTAL BALANCE
        
        balance = database.get_balance()

        self.balance_card = self.create_stat_card(
            "Current Balance",
            f"GHS {balance:,.2f}",
            "#3b82f6"
        )

        self.stats_layout.addWidget(self.balance_card)

        
        # TOTAL INCOME
    
        income = database.get_total_income()

        self.income_card = self.create_stat_card(
            "Total Income",
            f"GHS {income:,.2f}",
            "#22c55e"
        )

        self.stats_layout.addWidget(self.income_card)

        
        # TOTAL EXPENSES
        expenses = database.get_total_expenses()

        self.expense_card = self.create_stat_card(
            "Total Expenses",
            f"GHS {expenses:,.2f}",
            "#ef4444"
        )

        self.stats_layout.addWidget(self.expense_card)

        self.main_layout.addLayout(self.stats_layout)

     
        # CHARTS LAYOUT
        
        self.charts_layout = QHBoxLayout()
        self.charts_layout.setSpacing(20)

        # PIE CHART CARD
        
        self.pie_chart_card = QFrame()
        self.pie_chart_card.setObjectName("chartCard")

        self.pie_layout = QVBoxLayout(self.pie_chart_card)

        self.pie_title = QLabel("Expense Breakdown")
        self.pie_title.setFont(QFont("Segoe UI", 16, QFont.Bold))

        self.pie_layout.addWidget(self.pie_title)

        # Matplotlib Figure
        self.pie_figure = Figure(facecolor="#1e293b")

        self.pie_canvas = FigureCanvas(self.pie_figure)

        self.pie_layout.addWidget(self.pie_canvas)

        self.charts_layout.addWidget(self.pie_chart_card)

        
        # LINE CHART CARD
        
        self.line_chart_card = QFrame()
        self.line_chart_card.setObjectName("chartCard")

        self.line_layout = QVBoxLayout(self.line_chart_card)

        self.line_title = QLabel("Monthly Expenses")
        self.line_title.setFont(QFont("Segoe UI", 16, QFont.Bold))

        self.line_layout.addWidget(self.line_title)

        self.line_figure = Figure(facecolor="#1e293b")

        self.line_canvas = FigureCanvas(self.line_figure)

        self.line_layout.addWidget(self.line_canvas)

        self.charts_layout.addWidget(self.line_chart_card)

        self.main_layout.addLayout(self.charts_layout)

        
        # LOAD CHARTS
        
        self.load_pie_chart()

        self.load_line_chart()

        
        # STYLES
        
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: white;
                font-family: Segoe UI;
            }

            QLabel {
                color: white;
            }

            QFrame {
                background-color: #1e293b;
                border-radius: 18px;
            }

            #chartCard {
                background-color: #1e293b;
                border-radius: 18px;
                padding: 10px;
            }
        """)

    # CREATE STAT CARD
    
    def create_stat_card(self, title, value, color):

        card = QFrame()

        layout = QVBoxLayout(card)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 12))

        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 22, QFont.Bold))

        value_label.setStyleSheet(f"""
            color: {color};
        """)

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        return card

    
    # LOAD PIE CHART
    
    def load_pie_chart(self):

        data = database.get_expenses_by_category()

        categories = []
        amounts = []

        for row in data:

            category = row[0]
            amount = row[1] / 100

            categories.append(category)
            amounts.append(amount)

        self.pie_figure.clear()

        ax = self.pie_figure.add_subplot(111)

        ax.pie(
            amounts,
            labels=categories,
            autopct="%1.1f%%"
        )

        ax.set_facecolor("#1e293b")

        self.pie_canvas.draw()

   
    # LOAD LINE CHART
   
    def load_line_chart(self):

        data = database.get_monthly_expenses()

        months = []
        expenses = []

        for row in data:

            month = row[0]
            amount = row[1] / 100

            months.append(month)
            expenses.append(amount)

        self.line_figure.clear()

        ax = self.line_figure.add_subplot(111)

        ax.plot(
            months,
            expenses,
            marker="o",
            linewidth=3
        )

        ax.set_title(
            "Monthly Expense Trend",
            color="white",
            fontsize=14
        )

        ax.set_xlabel(
            "Month",
            color="white"
        )

        ax.set_ylabel(
            "Expenses (GHS)",
            color="white"
        )

        ax.tick_params(colors="white")

        ax.set_facecolor("#1e293b")

        self.line_figure.patch.set_facecolor("#1e293b")

        self.line_canvas.draw()