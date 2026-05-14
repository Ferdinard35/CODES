from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

import database


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        
        # MAIN LAYOUT
        
        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.main_layout.setSpacing(25)

        
        # TITLE
        
        self.title = QLabel("Finance Dashboard")
        self.title.setFont(QFont("Segoe UI", 24, QFont.Bold))

        self.main_layout.addWidget(self.title)

        
        # SUMMARY CARDS LAYOUT
       
        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(20)

        
        # BALANCE CARD
        
        balance = database.get_balance()

        self.balance_card = self.create_card(
            "Current Balance",
            f"GHS {balance:,.2f}",
            "#3b82f6"
        )

        self.cards_layout.addWidget(self.balance_card)

        
        # INCOME CARD
        
        income = database.get_total_income()

        self.income_card = self.create_card(
            "Total Income",
            f"GHS {income:,.2f}",
            "#22c55e"
        )

        self.cards_layout.addWidget(self.income_card)

       
        # EXPENSE CARD

        expenses = database.get_total_expenses()

        self.expense_card = self.create_card(
            "Total Expenses",
            f"GHS {expenses:,.2f}",
            "#ef4444"
        )

        self.cards_layout.addWidget(self.expense_card)

        # ADD CARDS TO MAIN LAYOUT
        self.main_layout.addLayout(self.cards_layout)

        
        # RECENT TRANSACTIONS TITLE
        
        self.recent_label = QLabel("Recent Transactions")
        self.recent_label.setFont(QFont("Segoe UI", 18, QFont.Bold))

        self.main_layout.addWidget(self.recent_label)

    
        # TABLE CONTAINER
        
        self.table_container = QFrame()
        self.table_container.setObjectName("tableContainer")

        self.table_layout = QVBoxLayout(self.table_container)
        self.table_layout.setContentsMargins(15, 15, 15, 15)

        
        # TABLE
        
        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "Date",
            "Category",
            "Description",
            "Amount",
            "Type"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.verticalHeader().setVisible(False)

        self.table.setAlternatingRowColors(True)

        self.table.setShowGrid(False)

        self.table.setMinimumHeight(300)

        self.table_layout.addWidget(self.table)

        self.main_layout.addWidget(self.table_container)

        
        # LOAD RECENT TRANSACTIONS
        
        self.load_recent_transactions()

       
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

            #tableContainer {
                background-color: #1e293b;
                border-radius: 18px;
            }

            QTableWidget {
                background-color: #1e293b;
                border: none;
                border-radius: 12px;
                font-size: 14px;
            }

            QHeaderView::section {
                background-color: #334155;
                color: white;
                border: none;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }

            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #334155;
            }

            QTableWidget::item:selected {
                background-color: #2563eb;
            }
        """)

   
    # CREATE SUMMARY CARD
   
    def create_card(self, title, amount, color):

        card = QFrame()

        layout = QVBoxLayout(card)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 12))

        amount_label = QLabel(amount)
        amount_label.setFont(QFont("Segoe UI", 22, QFont.Bold))

        amount_label.setStyleSheet(f"""
            color: {color};
        """)

        layout.addWidget(title_label)
        layout.addWidget(amount_label)

        return card

   
    # LOAD RECENT TRANSACTIONS
  
    def load_recent_transactions(self):

        transactions = database.get_recent_transactions()

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(transactions):

            self.table.insertRow(row_number)

            date = row_data[1]
            category = row_data[2]
            description = row_data[3]
            amount_cents = row_data[4]
            trans_type = row_data[5]

            amount = amount_cents / 100

            data = [
                date,
                category,
                description,
                f"GHS {amount:,.2f}",
                trans_type
            ]

            for column_number, data_item in enumerate(data):

                item = QTableWidgetItem(data_item)

                item.setTextAlignment(Qt.AlignCenter)

                # COLOR CODE
                if column_number == 3 or column_number == 4:

                    if trans_type == "Income":
                        item.setForeground(QColor("#22c55e"))

                    else:
                        item.setForeground(QColor("#ef4444"))

                self.table.setItem(
                    row_number,
                    column_number,
                    item
                )