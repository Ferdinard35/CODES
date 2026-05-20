from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
import database
from refresh import refresh_manager


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        # Outer scroll area so nothing gets clipped
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        container = QWidget()
        self.main_layout = QVBoxLayout(container)
        self.main_layout.setContentsMargins(36, 36, 36, 36)
        self.main_layout.setSpacing(0)

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

        # TITLE
        title = QLabel("Finance Dashboard")
        title.setObjectName("PageTitle")
        self.main_layout.addWidget(title)
        self.main_layout.addSpacing(4)

        subtitle = QLabel("A quick view of your balance, totals, and latest transaction activity.")
        subtitle.setObjectName("Subtitle")
        self.main_layout.addWidget(subtitle)
        self.main_layout.addSpacing(20)

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
        self.main_layout.addSpacing(24)

        # ── RECENT TRANSACTIONS ──
        recent_label = QLabel("Recent Transactions")
        recent_label.setObjectName("SectionTitle")
        self.main_layout.addWidget(recent_label)
        self.main_layout.addSpacing(10)

        # TABLE — no wrapper frame, table IS the card visually
        self.table = QTableWidget()
        self.table.setObjectName("DashTable")
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Date", "Category", "Description", "Amount", "Type"
        ])
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        header = self.table.horizontalHeader()
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
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.main_layout.addWidget(self.table)
        self.main_layout.addStretch()

        self.refresh_data()
        refresh_manager.data_changed.connect(self.refresh_data)

    def _create_card(self, title, accent):
        card = QFrame()
        card.setObjectName("Card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 20, 24, 20)
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
        self.balance_value.setText(f"GHS {database.get_balance():,.2f}")
        self.income_value.setText(f"GHS {database.get_total_income():,.2f}")
        self.expense_value.setText(f"GHS {database.get_total_expenses():,.2f}")
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

        # Fit table height exactly to rows — no overflow, no gap
        self.table.resizeRowsToContents()
        total_h = self.table.horizontalHeader().height() + 2
        for i in range(self.table.rowCount()):
            total_h += self.table.rowHeight(i)
        self.table.setFixedHeight(total_h)
