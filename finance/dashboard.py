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

from refresh import refresh_manager


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

    
        # MAIN LAYOUT
        
        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            25,
            25,
            25,
            25
        )

        self.main_layout.setSpacing(25)

    
        # TITLE
    
        self.title = QLabel(
            "Finance Dashboard"
        )

        self.title.setFont(
            QFont(
                "Segoe UI",
                24,
                QFont.Bold
            )
        )

        self.main_layout.addWidget(
            self.title
        )


        # SUMMARY CARDS LAYOUT
        
        self.cards_layout = QHBoxLayout()

        self.cards_layout.setSpacing(20)

        self.main_layout.addLayout(
            self.cards_layout
        )


        # CREATE CARDS
        
        self.balance_card, self.balance_value = (
            self.create_card(
                "Current Balance",
                "#3b82f6"
            )
        )

        self.income_card, self.income_value = (
            self.create_card(
                "Total Income",
                "#22c55e"
            )
        )

        self.expense_card, self.expense_value = (
            self.create_card(
                "Total Expenses",
                "#ef4444"
            )
        )

        # ADD CARDS
        self.cards_layout.addWidget(
            self.balance_card
        )

        self.cards_layout.addWidget(
            self.income_card
        )

        self.cards_layout.addWidget(
            self.expense_card
        )

        
        # RECENT TRANSACTIONS TITLE
        self.recent_label = QLabel(
            "Recent Transactions"
        )

        self.recent_label.setFont(
            QFont(
                "Segoe UI",
                18,
                QFont.Bold
            )
        )

        self.main_layout.addWidget(
            self.recent_label
        )


        # TABLE CONTAINER
        
        self.table_container = QFrame()

        self.table_container.setObjectName(
            "tableContainer"
        )

        self.table_layout = QVBoxLayout(
            self.table_container
        )

        self.table_layout.setContentsMargins(
            15,
            15,
            15,
            15
        )

    
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

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.setShowGrid(False)

        self.table.setMinimumHeight(300)

        self.table_layout.addWidget(
            self.table
        )

        self.main_layout.addWidget(
            self.table_container
        )

        
        # LOAD DATA
        
        self.refresh_data()

        
        # AUTO REFRESH
        
        refresh_manager.data_changed.connect(
            self.refresh_data
        )

        
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
    # CREATE CARD
    
    def create_card(
        self,
        title,
        color
    ):

        card = QFrame()

        layout = QVBoxLayout(card)

        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        layout.setSpacing(10)

        title_label = QLabel(title)

        title_label.setFont(
            QFont(
                "Segoe UI",
                12
            )
        )

        value_label = QLabel("GHS 0.00")

        value_label.setFont(
            QFont(
                "Segoe UI",
                22,
                QFont.Bold
            )
        )

        value_label.setStyleSheet(f"""
            color: {color};
        """)

        layout.addWidget(title_label)

        layout.addWidget(value_label)

        return card, value_label

    
    # REFRESH DATA
   
    def refresh_data(self):

        # LOAD CARD DATA
        balance = database.get_balance()

        income = database.get_total_income()

        expenses = database.get_total_expenses()

        self.balance_value.setText(
            f"GHS {balance:,.2f}"
        )

        self.income_value.setText(
            f"GHS {income:,.2f}"
        )

        self.expense_value.setText(
            f"GHS {expenses:,.2f}"
        )

        # LOAD TABLE
        self.load_recent_transactions()

    
    # LOAD RECENT TRANSACTIONS
    
    def load_recent_transactions(self):

        transactions = (
            database.get_recent_transactions()
        )

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(
            transactions
        ):

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

            for column_number, data_item in enumerate(
                data
            ):

                item = QTableWidgetItem(
                    data_item
                )

                item.setTextAlignment(
                    Qt.AlignCenter
                )

                
                # COLOR CODING
               
                if column_number in [3, 4]:

                    if trans_type == "Income":

                        item.setForeground(
                            QColor("#22c55e")
                        )

                    else:

                        item.setForeground(
                            QColor("#ef4444")
                        )

                self.table.setItem(
                    row_number,
                    column_number,
                    item
                )