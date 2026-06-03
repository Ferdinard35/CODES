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
from table_utils import RoundedTableWidget, fit_table_height_to_rows


def _fit(table):
    fit_table_height_to_rows(table)


class HistoryPage(QWidget):

    def __init__(self):
        super().__init__()
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        ctr = QWidget()
        self.ml = QVBoxLayout(ctr)
        self.ml.setContentsMargins(36, 36, 36, 36)
        self.ml.setSpacing(0)
        scroll.setWidget(ctr)
        outer.addWidget(scroll)

        # Header
        hdr = QHBoxLayout()
        left = QVBoxLayout(); left.setSpacing(4)
        title = QLabel("Transaction History"); title.setObjectName("PageTitle")
        sub = QLabel("Search, review, edit, and remove saved transaction records.")
        sub.setObjectName("Subtitle")
        left.addWidget(title); left.addWidget(sub)

        self.export_btn = QPushButton("  ↓  Export CSV")
        self.export_btn.setObjectName("SuccessButton")
        self.export_btn.setMinimumHeight(40)
        self.export_btn.setMinimumWidth(140)
        self.export_btn.setCursor(Qt.PointingHandCursor)
        self.export_btn.clicked.connect(self.export_csv)

        hdr.addLayout(left); hdr.addStretch(); hdr.addWidget(self.export_btn)
        self.ml.addLayout(hdr)
        self.ml.addSpacing(18)

        # Filter
        frow = QHBoxLayout(); frow.setSpacing(12)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search category or description...")
        self.search_input.setMinimumHeight(40)
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All", "Income", "Expense"])
        self.type_filter.setMinimumHeight(40)
        self.type_filter.setFixedWidth(140)
        frow.addWidget(self.search_input); frow.addWidget(self.type_filter)
        self.ml.addLayout(frow)
        self.ml.addSpacing(14)

        # Table
        self.table = RoundedTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Date", "Category", "Description",
            "Amount", "Type", "Edit", "Delete"
        ])
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        hd = self.table.horizontalHeader()
        hd.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hd.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        hd.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        hd.setSectionResizeMode(3, QHeaderView.Stretch)
        hd.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        hd.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        hd.setSectionResizeMode(6, QHeaderView.Fixed)
        hd.setSectionResizeMode(7, QHeaderView.Fixed)
        # Give columns 6+7 just enough room for the compact buttons + padding
        hd.resizeSection(6, 90)
        hd.resizeSection(7, 104)

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Row height — give buttons a little breathing room
        self.table.verticalHeader().setDefaultSectionSize(50)

        self.ml.addWidget(self.table)
        self.ml.addStretch()

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
        search = self.search_input.text().strip()
        ftype  = self.type_filter.currentText()
        rows   = database.search_transactions(search, ftype)

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
                        QColor("#22c55e") if ttype == "Income" else QColor("#ef4444"))
                self.table.setItem(rn, col, item)

            # Compact Edit button — outline style, fills on hover via CSS
            eb = QPushButton("Edit")
            eb.setObjectName("EditBtn")
            eb.setCursor(Qt.PointingHandCursor)
            eb.clicked.connect(lambda _, d=row: self.edit_transaction(d))
            self.table.setCellWidget(rn, 6, self._center(eb))

            # Compact Delete button
            db = QPushButton("Delete")
            db.setObjectName("DeleteBtn")
            db.setCursor(Qt.PointingHandCursor)
            db.clicked.connect(lambda _, i=tid: self.delete_transaction(i))
            self.table.setCellWidget(rn, 7, self._center(db))

        _fit(self.table)

    def _center(self, widget):
        """Center a widget inside a transparent cell container."""
        wrap = QWidget()
        wrap.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(wrap)
        lay.setContentsMargins(6, 6, 6, 6)
        lay.setAlignment(Qt.AlignCenter)
        lay.addWidget(widget)
        return wrap

    def delete_transaction(self, tid):
        reply = QMessageBox.question(
            self, "Delete", "Delete this transaction?",
            QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            database.delete_transaction(tid)
            refresh_manager.data_changed.emit()

    def edit_transaction(self, transaction):
        dlg = EditTransactionDialog(transaction)
        if dlg.exec():
            self.load_transactions()
