from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QMessageBox,
    QHeaderView,
    QAbstractItemView,
    QFrame,
    QLineEdit,
    QComboBox,
    QSizePolicy
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

import database
from refresh import refresh_manager
from edit_transaction_dialog import EditTransactionDialog
from export_utils import export_transactions_to_csv
from table_utils import fit_table_height_to_rows


class HistoryPage(QWidget):

    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(36, 36, 36, 36)
        self.main_layout.setSpacing(6)

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
        self.export_btn.setMinimumHeight(38)
        self.export_btn.setMinimumWidth(130)
        self.export_btn.setCursor(Qt.PointingHandCursor)
        self.export_btn.clicked.connect(self.export_csv)

        header_row.addLayout(title_col)
        header_row.addStretch()
        header_row.addWidget(self.export_btn)
        self.main_layout.addLayout(header_row)

        self.main_layout.addSpacing(14)

        # ── FILTER BAR ──
        filter_card = QFrame()
        filter_card.setObjectName("FormCard")
        filter_layout = QHBoxLayout(filter_card)
        filter_layout.setContentsMargins(16, 12, 16, 12)
        filter_layout.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search category or description...")
        self.search_input.setMinimumHeight(38)

        self.type_filter = QComboBox()
        self.type_filter.addItems(["All", "Income", "Expense"])
        self.type_filter.setMinimumHeight(38)
        self.type_filter.setFixedWidth(130)

        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(self.type_filter)
        self.main_layout.addWidget(filter_card)

        self.search_input.textChanged.connect(self.apply_filters)
        self.type_filter.currentTextChanged.connect(self.apply_filters)

        # ── TABLE CONTAINER ──
        self.container = QFrame()
        self.container.setObjectName("TableCard")
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Date", "Category", "Description",
            "Amount", "Type", "Edit", "Delete"
        ])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)

        container_layout.addWidget(self.table)
        self.main_layout.addWidget(self.container)

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

            # Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.setObjectName("SecondaryButton")
            edit_btn.setFixedHeight(30)
            edit_btn.setCursor(Qt.PointingHandCursor)
            edit_btn.clicked.connect(
                lambda _, data=row_data: self.edit_transaction(data)
            )
            self.table.setCellWidget(row_number, 6, edit_btn)

            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.setObjectName("DangerButton")
            delete_btn.setFixedHeight(30)
            delete_btn.setCursor(Qt.PointingHandCursor)
            delete_btn.clicked.connect(
                lambda _, tid=transaction_id: self.delete_transaction(tid)
            )
            self.table.setCellWidget(row_number, 7, delete_btn)

        fit_table_height_to_rows(self.table, min_rows=0, max_rows=14)

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
