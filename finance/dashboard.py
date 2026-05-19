from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QSizePolicy
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

import database
from refresh import refresh_manager
from table_utils import fit_table_height_to_rows


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(36, 36, 36, 36)
        self.main_layout.setSpacing(6)

        # TITLE
        title = QLabel("Finance Dashboard")
        title.setObjectName("PageTitle")
        self.main_layout.addWidget(title)

        subtitle = QLabel("A quick view of your balance, totals, and latest transaction activity.")
        subtitle.setObjectName("Subtitle")
        self.main_layout.addWidget(subtitle)

        self.main_layout.addSpacing(16)

        # ── SUMMARY CARDS ──
        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)

        self.balance_card, self.balance_value = self._create_card("Current Balance", "primary")
        self.income_card,  self.income_value  = self._create_card("Total Income",    "success")
        self.expense_card, self.expense_value = self._create_card("Total Expenses",  "danger")

        cards_row.addWidget(self.balance_card)
        cards_row.addWidget(self.income_card)
        cards_row.addWidget(self.expense_card)
        self.main_layout.addLayout(cards_row)

        self.main_layout.addSpacing(8)

        # ── RECENT TRANSACTIONS ──
        recent_label = QLabel("Recent Transactions")
        recent_label.setObjectName("SectionTitle")
        self.main_layout.addWidget(recent_label)

        self.main_layout.addSpacing(6)

        # TABLE CONTAINER
        self.table_container = QFrame()
        self.table_container.setObjectName("TableCard")
        self.table_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        table_layout = QVBoxLayout(self.table_container)
        table_layout.setContentsMargins(0, 0, 0, 0)

        # TABLE
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Date", "Category", "Description", "Amount", "Type"
        ])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)

        table_layout.addWidget(self.table)
        self.main_layout.addWidget(self.table_container)

        self.refresh_data()
        refresh_manager.data_changed.connect(self.refresh_data)

    def _create_card(self, title, accent):
        card = QFrame()
        card.setObjectName("Card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(8)

        title_lbl = QLabel(title.upper())
        title_lbl.setObjectName("MetricTitle")

        value_lbl = QLabel("GHS 0.00")
        value_lbl.setObjectName("MetricValue")
        value_lbl.setProperty("accent", accent)

        layout.addWidget(title_lbl)
        layout.addWidget(value_lbl)

        return card, value_lbl

    def refresh_data(self):
        balance  = database.get_balance()
        income   = database.get_total_income()
        expenses = database.get_total_expenses()

        self.balance_value.setText(f"GHS {balance:,.2f}")
        self.income_value.setText(f"GHS {income:,.2f}")
        self.expense_value.setText(f"GHS {expenses:,.2f}")

        self.load_recent_transactions()

    def load_recent_transactions(self):
        transactions = database.get_transactions()
        self.table.setRowCount(0)

        for row_number, row_data in enumerate(transactions):
            self.table.insertRow(row_number)

            date        = row_data[1]
            category    = row_data[2]
            description = row_data[3]
            amount      = row_data[4] / 100
            trans_type  = row_data[5]

            values = [date, category, description, f"GHS {amount:,.2f}", trans_type]

            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if col in [3, 4]:
                    item.setForeground(
                        QColor("#22c55e") if trans_type == "Income" else QColor("#ef4444")
                    )
                self.table.setItem(row_number, col, item)

        fit_table_height_to_rows(self.table, min_rows=0, max_rows=8)
