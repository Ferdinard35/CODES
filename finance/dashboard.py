from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import database
from refresh import refresh_manager


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        container = QWidget()
        self.main_layout = QVBoxLayout(container)
        self.main_layout.setContentsMargins(36, 36, 36, 36)
        self.main_layout.setSpacing(0)

        scroll.setWidget(container)
        outer.addWidget(scroll)

        # TITLE
        title = QLabel("Finance Dashboard")
        title.setObjectName("PageTitle")
        self.main_layout.addWidget(title)
        self.main_layout.addSpacing(4)

        subtitle = QLabel("A quick view of your balance, totals, and latest transaction activity.")
        subtitle.setObjectName("Subtitle")
        self.main_layout.addWidget(subtitle)
        self.main_layout.addSpacing(20)

        # ── CARDS ──
        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)
        self.balance_card, self.balance_value = self._card("Current Balance", "primary")
        self.income_card,  self.income_value  = self._card("Total Income",    "success")
        self.expense_card, self.expense_value = self._card("Total Expenses",  "danger")
        cards_row.addWidget(self.balance_card)
        cards_row.addWidget(self.income_card)
        cards_row.addWidget(self.expense_card)
        self.main_layout.addLayout(cards_row)
        self.main_layout.addSpacing(24)

        # ── RECENT TRANSACTIONS ──
        lbl = QLabel("Recent Transactions")
        lbl.setObjectName("SectionTitle")
        self.main_layout.addWidget(lbl)
        self.main_layout.addSpacing(10)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Date", "Category", "Description", "Amount", "Type"])
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        hdr = self.table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(2, QHeaderView.Stretch)
        hdr.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(4, QHeaderView.ResizeToContents)

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

    def _card(self, title, accent):
        card = QFrame()
        card.setObjectName("Card")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(24, 20, 24, 20)
        lay.setSpacing(8)

        t = QLabel(title.upper())
        t.setObjectName("MetricTitle")

        v = QLabel("GHS 0.00")
        v.setObjectName("MetricValue")
        v.setProperty("accent", accent)

        lay.addWidget(t)
        lay.addWidget(v)
        return card, v

    def refresh_data(self):
        self.balance_value.setText(f"GHS {database.get_balance():,.2f}")
        self.income_value.setText(f"GHS {database.get_total_income():,.2f}")
        self.expense_value.setText(f"GHS {database.get_total_expenses():,.2f}")
        self._load_table()

    def _load_table(self):
        txns = database.get_transactions()
        self.table.setRowCount(0)

        for rn, row in enumerate(txns):
            self.table.insertRow(rn)
            date   = row[1]
            cat    = row[2]
            desc   = row[3]
            amount = row[4] / 100
            ttype  = row[5]

            for col, val in enumerate([date, cat, desc, f"GHS {amount:,.2f}", ttype]):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if col in [3, 4]:
                    item.setForeground(
                        QColor("#22c55e") if ttype == "Income" else QColor("#ef4444")
                    )
                self.table.setItem(rn, col, item)

        # Fit height — table clips itself neatly
        self.table.resizeRowsToContents()
        h = self.table.horizontalHeader().height() + 2
        for i in range(self.table.rowCount()):
            h += self.table.rowHeight(i)
        if self.table.rowCount() == 0:
            h += 60
        self.table.setFixedHeight(h)
