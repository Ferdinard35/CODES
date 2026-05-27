from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QMessageBox, QHeaderView,
    QAbstractItemView, QFrame, QLineEdit, QComboBox,
    QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import database
from refresh import refresh_manager
from edit_transaction_dialog import EditTransactionDialog
from export_utils import export_transactions_to_csv


class HistoryPage(QWidget):

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

        # ── HEADER ──
        header_row = QHBoxLayout()
        left = QVBoxLayout()
        left.setSpacing(4)
        title = QLabel("Transaction History")
        title.setObjectName("PageTitle")
        subtitle = QLabel("Search, review, edit, and remove saved transaction records.")
        subtitle.setObjectName("Subtitle")
        left.addWidget(title)
        left.addWidget(subtitle)

        self.export_btn = QPushButton("  ↓  Export CSV")
        self.export_btn.setObjectName("SuccessButton")
        self.export_btn.setMinimumHeight(40)
        self.export_btn.setMinimumWidth(140)
        self.export_btn.setCursor(Qt.PointingHandCursor)
        self.export_btn.clicked.connect(self.export_csv)

        header_row.addLayout(left)
        header_row.addStretch()
        header_row.addWidget(self.export_btn)
        self.main_layout.addLayout(header_row)
        self.main_layout.addSpacing(18)

        # ── FILTER BAR ──
        filter_row = QHBoxLayout()
        filter_row.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search category or description...")
        self.search_input.setMinimumHeight(40)

        self.type_filter = QComboBox()
        self.type_filter.addItems(["All", "Income", "Expense"])
        self.type_filter.setMinimumHeight(40)
        self.type_filter.setFixedWidth(140)

        filter_row.addWidget(self.search_input)
        filter_row.addWidget(self.type_filter)
        self.main_layout.addLayout(filter_row)
        self.main_layout.addSpacing(14)

        # ── TABLE ──
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Date", "Category", "Description",
            "Amount", "Type", "Edit", "Delete"
        ])
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        hdr = self.table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(3, QHeaderView.Stretch)
        hdr.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(6, QHeaderView.Fixed)
        hdr.setSectionResizeMode(7, QHeaderView.Fixed)
        hdr.resizeSection(6, 90)
        hdr.resizeSection(7, 100)

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.main_layout.addWidget(self.table)
        self.main_layout.addStretch()

        self.search_input.textChanged.connect(self.apply_filters)
        self.type_filter.currentTextChanged.connect(self.apply_filters)
        self.load_transactions()

        try:
            refresh_manager.data_changed.disconnect(self.load_transactions)
        except Exception:
            pass
        refresh_manager.data_changed.connect(self.load_transactions)

    def export_csv(self):
        filename = export_transactions_to_csv()
        QMessageBox.information(self, "Export Complete", f"Data exported:\n{filename}")

    def load_transactions(self):
        self.apply_filters()

    def apply_filters(self):
        search_text = self.search_input.text().strip()
        trans_type  = self.type_filter.currentText()
        rows        = database.search_transactions(search_text, trans_type)

        self.table.setRowCount(0)

        for rn, row in enumerate(rows):
            self.table.insertRow(rn)

            tid    = row[0]
            date   = row[1] or ""
            cat    = row[2] or ""
            desc   = row[3] or ""
            amount = (row[4] or 0) / 100
            ttype  = row[5] or ""

            for col, val in enumerate([str(tid), date, cat, desc,
                                        f"GHS {amount:,.2f}", ttype]):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if col == 4:
                    item.setForeground(
                        QColor("#22c55e") if ttype == "Income" else QColor("#ef4444")
                    )
                self.table.setItem(rn, col, item)

            # ── Edit button ──
            edit_btn = QPushButton("Edit")
            edit_btn.setObjectName("SecondaryButton")
            edit_btn.setFixedHeight(34)
            edit_btn.setMinimumWidth(70)
            edit_btn.setCursor(Qt.PointingHandCursor)
            edit_btn.clicked.connect(lambda _, d=row: self.edit_transaction(d))
            self.table.setCellWidget(rn, 6, self._wrap(edit_btn))

            # ── Delete button ──
            del_btn = QPushButton("Delete")
            del_btn.setObjectName("DangerButton")
            del_btn.setFixedHeight(34)
            del_btn.setMinimumWidth(78)
            del_btn.setCursor(Qt.PointingHandCursor)
            del_btn.clicked.connect(lambda _, i=tid: self.delete_transaction(i))
            self.table.setCellWidget(rn, 7, self._wrap(del_btn))

        # ── Fit table height precisely ──
        self.table.resizeRowsToContents()
        h = self.table.horizontalHeader().height() + 2
        for i in range(self.table.rowCount()):
            h += self.table.rowHeight(i)
        if self.table.rowCount() == 0:
            h += 60
        self.table.setFixedHeight(h)

    def _wrap(self, widget):
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(6, 3, 6, 3)
        lay.setAlignment(Qt.AlignCenter)
        lay.addWidget(widget)
        return w

    def delete_transaction(self, tid):
        reply = QMessageBox.question(
            self, "Delete", "Delete this transaction?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            database.delete_transaction(tid)
            refresh_manager.data_changed.emit()

    def edit_transaction(self, transaction):
        from edit_transaction_dialog import EditTransactionDialog
        dlg = EditTransactionDialog(transaction)
        if dlg.exec():
            self.load_transactions()
