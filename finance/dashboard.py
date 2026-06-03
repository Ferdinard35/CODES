from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import database
from refresh import refresh_manager
from table_utils import RoundedTableWidget, fit_table_height_to_rows


def _fit(table):
    fit_table_height_to_rows(table)


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        ctr = QWidget()
        ml  = QVBoxLayout(ctr)
        ml.setContentsMargins(36, 36, 36, 36)
        ml.setSpacing(0)

        scroll.setWidget(ctr)
        outer.addWidget(scroll)

        ml.addWidget(self._lbl("Finance Dashboard", "PageTitle"))
        ml.addSpacing(4)
        ml.addWidget(self._lbl(
            "A quick view of your balance, totals, and latest transaction activity.", "Subtitle"))
        ml.addSpacing(20)

        row = QHBoxLayout()
        row.setSpacing(16)
        self.balance_card, self.balance_val = self._card("Current Balance", "primary")
        self.income_card,  self.income_val  = self._card("Total Income",    "success")
        self.expense_card, self.expense_val = self._card("Total Expenses",  "danger")
        row.addWidget(self.balance_card)
        row.addWidget(self.income_card)
        row.addWidget(self.expense_card)
        ml.addLayout(row)
        ml.addSpacing(24)

        ml.addWidget(self._lbl("Recent Transactions", "SectionTitle"))
        ml.addSpacing(10)

        self.table = self._make_table(["Date", "Category", "Description", "Amount", "Type"])
        hdr = self.table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(2, QHeaderView.Stretch)
        hdr.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        ml.addWidget(self.table)
        ml.addStretch()

        self.refresh_data()
        refresh_manager.data_changed.connect(self.refresh_data)

    def _lbl(self, text, name):
        l = QLabel(text); l.setObjectName(name); return l

    def _card(self, title, accent):
        card = QFrame(); card.setObjectName("Card")
        lay  = QVBoxLayout(card)
        lay.setContentsMargins(24, 20, 24, 20); lay.setSpacing(8)
        t = QLabel(title.upper()); t.setObjectName("MetricTitle")
        v = QLabel("GHS 0.00");    v.setObjectName("MetricValue"); v.setProperty("accent", accent)
        lay.addWidget(t); lay.addWidget(v)
        return card, v

    def _make_table(self, headers):
        t = RoundedTableWidget()
        t.setColumnCount(len(headers))
        t.setHorizontalHeaderLabels(headers)
        t.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        t.setSelectionBehavior(QAbstractItemView.SelectRows)
        t.setEditTriggers(QAbstractItemView.NoEditTriggers)
        t.verticalHeader().setVisible(False)
        t.setAlternatingRowColors(True)
        t.setShowGrid(False)
        t.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        t.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        return t

    def refresh_data(self):
        self.balance_val.setText(f"GHS {database.get_balance():,.2f}")
        self.income_val.setText(f"GHS {database.get_total_income():,.2f}")
        self.expense_val.setText(f"GHS {database.get_total_expenses():,.2f}")
        self._load_table()

    def _load_table(self):
        txns = database.get_transactions()
        self.table.setRowCount(0)
        for rn, row in enumerate(txns):
            self.table.insertRow(rn)
            date, cat, desc = row[1], row[2], row[3]
            amount = row[4] / 100
            ttype  = row[5]
            for col, val in enumerate([date, cat, desc, f"GHS {amount:,.2f}", ttype]):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if col in [3, 4]:
                    item.setForeground(
                        QColor("#22c55e") if ttype == "Income" else QColor("#ef4444"))
                self.table.setItem(rn, col, item)
        _fit(self.table)
