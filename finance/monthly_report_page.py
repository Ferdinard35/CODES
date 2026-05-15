from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame
)

from PySide6.QtGui import QFont
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import database


class MonthlyReportPage(QWidget):

    def __init__(self):
        super().__init__()

        
        # MAIN LAYOUT
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(25, 25, 25, 25)
        self.layout.setSpacing(20)

        # TITLE
        self.title = QLabel("Monthly Financial Reports")
        self.title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.layout.addWidget(self.title)

       
        # SUMMARY CARDS
        
        self.cards_layout = QHBoxLayout()

        self.best_month_card = self.create_card("Best Month", "-", "#22c55e")
        self.worst_month_card = self.create_card("Worst Month", "-", "#ef4444")
        self.avg_card = self.create_card("Avg Monthly Savings", "-", "#3b82f6")

        self.cards_layout.addWidget(self.best_month_card)
        self.cards_layout.addWidget(self.worst_month_card)
        self.cards_layout.addWidget(self.avg_card)

        self.layout.addLayout(self.cards_layout)

        
        # CHARTS AREA
   
        self.charts_layout = QHBoxLayout()

        # LINE CHART (Income vs Expense)
        self.line_frame = QFrame()
        self.line_layout = QVBoxLayout(self.line_frame)

        self.line_title = QLabel("Income vs Expenses")
        self.line_title.setFont(QFont("Segoe UI", 14, QFont.Bold))

        self.line_fig = Figure(facecolor="#1e293b")
        self.line_canvas = FigureCanvas(self.line_fig)

        self.line_layout.addWidget(self.line_title)
        self.line_layout.addWidget(self.line_canvas)

        # NET BALANCE CHART
        self.net_frame = QFrame()
        self.net_layout = QVBoxLayout(self.net_frame)

        self.net_title = QLabel("Net Savings Trend")
        self.net_title.setFont(QFont("Segoe UI", 14, QFont.Bold))

        self.net_fig = Figure(facecolor="#1e293b")
        self.net_canvas = FigureCanvas(self.net_fig)

        self.net_layout.addWidget(self.net_title)
        self.net_layout.addWidget(self.net_canvas)

        self.charts_layout.addWidget(self.line_frame)
        self.charts_layout.addWidget(self.net_frame)

        self.layout.addLayout(self.charts_layout)

        # LOAD DATA
        self.load_data()

        # STYLE
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: white;
                font-family: Segoe UI;
            }

            QFrame {
                background-color: #1e293b;
                border-radius: 18px;
                padding: 10px;
            }

            QLabel {
                color: white;
            }
        """)

   
    # CARD BUILDER
    
    def create_card(self, title, value, color):

        card = QFrame()
        layout = QVBoxLayout(card)

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 11))

        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        value_label.setStyleSheet(f"color:{color};")

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        return card


    # LOAD DATA
    
    def load_data(self):

        data = database.get_monthly_summary()

        months = []
        income = []
        expenses = []
        net = []

        for row in data:

            month = row[0]
            inc = row[1] / 100
            exp = row[2] / 100

            months.append(month)
            income.append(inc)
            expenses.append(exp)
            net.append(inc - exp)

      
        # BEST / WORST MONTH
        
        if net:

            best_index = net.index(max(net))
            worst_index = net.index(min(net))

            self.update_card(self.best_month_card, "Best Month", f"{months[best_index]} (+GHS {net[best_index]:,.2f})", "#22c55e")
            self.update_card(self.worst_month_card, "Worst Month", f"{months[worst_index]} (GHS {net[worst_index]:,.2f})", "#ef4444")

            avg = sum(net) / len(net)
            self.update_card(self.avg_card, "Avg Monthly Savings", f"GHS {avg:,.2f}", "#3b82f6")

        
        # LINE CHART (INCOME vs EXPENSE)
        
        self.line_fig.clear()
        ax1 = self.line_fig.add_subplot(111)

        ax1.plot(months, income, marker="o", label="Income")
        ax1.plot(months, expenses, marker="o", label="Expenses")

        ax1.set_title("Monthly Income vs Expenses", color="white")
        ax1.tick_params(colors="white")
        ax1.legend()
        ax1.grid(True)

        self.line_canvas.draw()

        
        # NET CHART
        
        self.net_fig.clear()
        ax2 = self.net_fig.add_subplot(111)

        ax2.plot(months, net, marker="o", color="green")

        ax2.set_title("Net Savings Trend", color="white")
        ax2.tick_params(colors="white")
        ax2.axhline(0, color="red", linestyle="--")

        self.net_canvas.draw()

    
    # UPDATE CARD TEXT
    
    def update_card(self, card, title, value, color):

        layout = card.layout()

        layout.itemAt(0).widget().setText(title)
        value_label = layout.itemAt(1).widget()
        value_label.setText(value)
        value_label.setStyleSheet(f"color:{color};")