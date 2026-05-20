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

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

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

        # ── HEADER ──
        header_row = QHBoxLayout()
        title_col = QVBoxLayout()
        title_col.setSpacing(4)

        title = QLabel("Transaction History")
        title.setObjectName("PageTitle")
        subtitle = QLabel("Search, review, edit, and remove saved transaction records.")
        subtitle.setObjectName("Subtitle")

        title_col.addWidget(title)
        title_col.addWidget(subtitle)

        self.export_btn = QPushButton("  ↓  Export CSV")
        self.export_btn.setObjectName("SuccessButton")
        self.export_btn.setMinimumHeight(40)
        self.export_btn.setMinimumWidth(140)
        self.export_btn.setCursor(Qt.PointingHandCursor)
        self.export_btn.clicked.connect(self.export_csv)

        header_row.addLayout(title_col)
        header_row.addStretch()
        header_row.addWidget(self.export_btn)
        self.main_layout.addLayout(header_row)
        self.main_layout.addSpacing(20)

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

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.Fixed)
        header.setSectionResizeMode(7, QHeaderView.Fixed)
        header.resizeSection(6, 80)
        header.resizeSection(7, 90)

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
        transactions = database.search_transactions(search_text, trans_type)

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(transactions):
            self.table.insertRow(row_number)

            transaction_id = row_data[0]
            date        = row_data[1] or ""
            category    = row_data[2] or ""
            description = row_data[3] or ""
            amount      = (row_data[4] or 0) / 100
            t_type      = row_data[5] or ""

            values = [
                str(transaction_id), date, category, description,
                f"GHS {amount:,.2f}", t_type
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if col == 4:
                    item.setForeground(
                        QColor("#22c55e") if t_type == "Income" else QColor("#ef4444")
                    )
                self.table.setItem(row_number, col, item)

            # Edit button — fixed width so text is always visible
            edit_btn = QPushButton("Edit")
            edit_btn.setObjectName("SecondaryButton")
            edit_btn.setFixedSize(72, 32)
            edit_btn.setCursor(Qt.PointingHandCursor)
            edit_btn.clicked.connect(
                lambda _, data=row_data: self.edit_transaction(data)
            )
            self.table.setCellWidget(row_number, 6, self._center_widget(edit_btn))

            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.setObjectName("DangerButton")
            delete_btn.setFixedSize(80, 32)
            delete_btn.setCursor(Qt.PointingHandCursor)
            delete_btn.clicked.connect(
                lambda _, tid=transaction_id: self.delete_transaction(tid)
            )
            self.table.setCellWidget(row_number, 7, self._center_widget(delete_btn))

        # Fit height to rows
        self.table.resizeRowsToContents()
        total_h = self.table.horizontalHeader().height() + 2
        for i in range(self.table.rowCount()):
            total_h += self.table.rowHeight(i)
        if self.table.rowCount() == 0:
            total_h += 60  # empty state height
        self.table.setFixedHeight(total_h)

    def _center_widget(self, widget):
        """Wrap a widget in a centered container so it sits nicely in the cell."""
        wrap = QWidget()
        layout = QHBoxLayout(wrap)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(widget)
        return wrap

    def delete_transaction(self, transaction_id):
        reply = QMessageBox.question(
            self, "Delete", "Are you sure you want to delete this transaction?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            database.delete_transaction(transaction_id)
            refresh_manager.data_changed.emit()

    def edit_transaction(self, transaction):
        dialog = EditTransactionDialog(transaction)
        if dialog.exec():
            self.load_transactions()
