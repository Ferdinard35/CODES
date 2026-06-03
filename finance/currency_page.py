"""
currency_page.py
================
UI page for the live currency converter.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QFrame, QSizePolicy, QScrollArea,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont

import database
from currency_converter import fetch_rates, convert, format_amount, SUPPORTED
from table_utils import RoundedTableWidget, fit_table_height_to_rows


# ── Background worker so the UI never freezes ──────────────────────
class FetchRatesWorker(QThread):
    rates_ready = Signal(dict)
    error       = Signal(str)

    def __init__(self, base="GHS"):
        super().__init__()
        self.base = base

    def run(self):
        try:
            rates = fetch_rates(self.base)
            self.rates_ready.emit(rates)
        except Exception as e:
            self.error.emit(str(e))


# ── Page ──────────────────────────────────────────────────────────
class CurrencyPage(QWidget):

    def __init__(self):
        super().__init__()
        self._rates = {}
        self._worker = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        container = QWidget()
        main = QVBoxLayout(container)
        main.setContentsMargins(36, 36, 36, 36)
        main.setSpacing(0)

        scroll.setWidget(container)
        outer.addWidget(scroll)

        # Title
        main.addWidget(self._lbl("Currency Converter", "PageTitle"))
        main.addSpacing(4)
        main.addWidget(self._lbl(
            "Convert amounts between currencies using live exchange rates.", "Subtitle"
        ))
        main.addSpacing(20)

        # ── Converter card ──
        conv_card = QFrame()
        conv_card.setObjectName("FormCard")
        conv = QVBoxLayout(conv_card)
        conv.setContentsMargins(28, 24, 28, 24)
        conv.setSpacing(16)

        # Row: amount + from + to
        input_row = QHBoxLayout()
        input_row.setSpacing(12)

        amount_col = QVBoxLayout()
        amount_col.setSpacing(6)
        amount_col.addWidget(self._lbl("AMOUNT", "FieldLabel"))
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        self.amount_input.setMinimumHeight(42)
        amount_col.addWidget(self.amount_input)

        from_col = QVBoxLayout()
        from_col.setSpacing(6)
        from_col.addWidget(self._lbl("FROM", "FieldLabel"))
        self.from_combo = QComboBox()
        self.from_combo.addItems(SUPPORTED)
        self.from_combo.setMinimumHeight(42)
        from_col.addWidget(self.from_combo)

        arrow = QLabel("→")
        arrow.setAlignment(Qt.AlignCenter)
        arrow.setStyleSheet("font-size:20px; color:#94a3b8; background:transparent; padding-top:24px;")

        to_col = QVBoxLayout()
        to_col.setSpacing(6)
        to_col.addWidget(self._lbl("TO", "FieldLabel"))
        self.to_combo = QComboBox()
        self.to_combo.addItems(SUPPORTED)
        self.to_combo.setCurrentIndex(1)   # USD by default
        self.to_combo.setMinimumHeight(42)
        to_col.addWidget(self.to_combo)

        input_row.addLayout(amount_col, 3)
        input_row.addLayout(from_col, 2)
        input_row.addWidget(arrow)
        input_row.addLayout(to_col, 2)
        conv.addLayout(input_row)

        # Convert button
        btn_row = QHBoxLayout()
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.setMinimumHeight(44)
        self.convert_btn.setMinimumWidth(160)
        self.convert_btn.setCursor(Qt.PointingHandCursor)
        self.convert_btn.clicked.connect(self.do_convert)

        self.status_lbl = QLabel("")
        self.status_lbl.setObjectName("Subtitle")

        btn_row.addWidget(self.convert_btn)
        btn_row.addSpacing(16)
        btn_row.addWidget(self.status_lbl)
        btn_row.addStretch()
        conv.addLayout(btn_row)

        # Result
        self.result_lbl = QLabel("")
        self.result_lbl.setObjectName("MetricValue")
        self.result_lbl.setProperty("accent", "primary")
        conv.addWidget(self.result_lbl)

        main.addWidget(conv_card)
        main.addSpacing(20)

        # ── Rate table card ──
        rates_title = self._lbl("Live Rates  (Base: GHS)", "SectionTitle")
        main.addWidget(rates_title)
        main.addSpacing(10)

        self.rate_table = RoundedTableWidget()
        self.rate_table.setColumnCount(3)
        self.rate_table.setHorizontalHeaderLabels(["Currency", "1 GHS =", "1 Unit → GHS"])
        self.rate_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        rh = self.rate_table.horizontalHeader()
        rh.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        rh.setSectionResizeMode(1, QHeaderView.Stretch)
        rh.setSectionResizeMode(2, QHeaderView.Stretch)

        self.rate_table.verticalHeader().setVisible(False)
        self.rate_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.rate_table.setShowGrid(False)
        self.rate_table.setAlternatingRowColors(True)
        self.rate_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        main.addWidget(self.rate_table)

        self.refresh_lbl = QLabel("")
        self.refresh_lbl.setObjectName("Subtitle")
        main.addSpacing(8)
        main.addWidget(self.refresh_lbl)

        refresh_btn = QPushButton("Refresh Rates")
        refresh_btn.setObjectName("SecondaryButton")
        refresh_btn.setMinimumHeight(38)
        refresh_btn.setFixedWidth(160)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.load_rates)
        main.addSpacing(8)
        main.addWidget(refresh_btn)
        main.addStretch()

        self.load_rates()

    # ── helpers ──
    def _lbl(self, text, obj_name):
        l = QLabel(text)
        l.setObjectName(obj_name)
        return l

    def load_rates(self):
        self.status_lbl.setText("Fetching live rates…")
        self._worker = FetchRatesWorker("GHS")
        self._worker.rates_ready.connect(self._on_rates)
        self._worker.error.connect(lambda e: self.status_lbl.setText(f"Offline – using fallback rates"))
        self._worker.start()

    def _on_rates(self, rates):
        self._rates = rates
        self.status_lbl.setText("")
        self.refresh_lbl.setText("Rates updated  ✓")
        self._populate_rate_table(rates)

    def _populate_rate_table(self, rates):
        self.rate_table.setRowCount(0)
        for i, (cur, rate) in enumerate(rates.items()):
            self.rate_table.insertRow(i)
            self.rate_table.setItem(i, 0, QTableWidgetItem(cur))
            self.rate_table.setItem(i, 1, QTableWidgetItem(f"{rate:.4f} {cur}"))
            inv = 1.0 / rate if rate else 0
            self.rate_table.setItem(i, 2, QTableWidgetItem(f"{inv:.4f} GHS"))

        fit_table_height_to_rows(self.rate_table)

    def do_convert(self):
        text = self.amount_input.text().strip()
        if not text:
            self.result_lbl.setText("Enter an amount first.")
            return
        try:
            amount = float(text)
        except ValueError:
            self.result_lbl.setText("Invalid amount.")
            return

        frm = self.from_combo.currentText()
        to  = self.to_combo.currentText()
        result = convert(amount, frm, to)
        self.result_lbl.setText(
            f"{format_amount(amount, frm)}  =  {format_amount(result, to)}"
        )
