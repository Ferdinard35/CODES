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
    QComboBox
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

import database
from refresh import refresh_manager
from edit_transaction_dialog import EditTransactionDialog


class HistoryPage(QWidget):

    def __init__(self):
        super().__init__()


        # MAIN LAYOUT
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.main_layout.setSpacing(20)

        
        # TITLE
        
        self.title = QLabel("Transaction History")
        self.title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.main_layout.addWidget(self.title)

        
        # FILTER BAR (SEARCH + TYPE)
    
        self.filter_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search category or description...")

        self.type_filter = QComboBox()
        self.type_filter.addItems(["All", "Income", "Expense"])

        self.filter_layout.addWidget(self.search_input)
        self.filter_layout.addWidget(self.type_filter)

        self.main_layout.addLayout(self.filter_layout)

        # CONNECT FILTERS
        self.search_input.textChanged.connect(self.apply_filters)
        self.type_filter.currentTextChanged.connect(self.apply_filters)

        
        # CONTAINER
        
        self.container = QFrame()
        self.container.setObjectName("container")

        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(20, 20, 20, 20)

        
        # TABLE
    
        self.table = QTableWidget()
        self.table.setColumnCount(8)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Date",
            "Category",
            "Description",
            "Amount",
            "Type",
            "Edit",
            "Delete"
        ])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setMinimumHeight(500)

        self.container_layout.addWidget(self.table)
        self.main_layout.addWidget(self.container)

        # LOAD DATA
        self.load_transactions()

        # AUTO REFRESH
        refresh_manager.data_changed.connect(self.load_transactions)


        # STYLES
        
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: white;
                font-family: Segoe UI;
            }

            QLineEdit, QComboBox {
                padding: 10px;
                border-radius: 8px;
                background-color: #1e293b;
                color: white;
                border: 1px solid #334155;
            }

            #container {
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
                padding: 12px;
                font-weight: bold;
            }

            QPushButton {
                color: white;
                border-radius: 8px;
                padding: 6px;
                font-weight: bold;
            }
        """)


    # LOAD ALL
    
    def load_transactions(self):
        self.apply_filters()

    
    # SEARCH + FILTER
    
    def apply_filters(self):

        search_text = self.search_input.text()
        trans_type = self.type_filter.currentText()

        transactions = database.search_transactions(
            search_text,
            trans_type
        )

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(transactions):

            self.table.insertRow(row_number)

            transaction_id = row_data[0]
            date = row_data[1]
            category = row_data[2]
            description = row_data[3]
            amount_cents = row_data[4]
            trans_type = row_data[5]

            amount = amount_cents / 100

            data = [
                str(transaction_id),
                date,
                category,
                description,
                f"GHS {amount:,.2f}",
                trans_type
            ]

            for col, value in enumerate(data):

                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)

                if col in [4, 5]:
                    item.setForeground(
                        QColor("#22c55e") if trans_type == "Income"
                        else QColor("#ef4444")
                    )

                self.table.setItem(row_number, col, item)

           
            # EDIT BUTTON
           
            edit_btn = QPushButton("Edit")
            edit_btn.setStyleSheet("background-color:#2563eb;")

            edit_btn.clicked.connect(
                self.make_edit_handler(row_data)
            )

            self.table.setCellWidget(row_number, 6, edit_btn)

          
            # DELETE BUTTON
            
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("background-color:#dc2626;")

            delete_btn.clicked.connect(
                lambda _, tid=transaction_id:
                self.delete_transaction(tid)
            )

            self.table.setCellWidget(row_number, 7, delete_btn)

    
    # SAFE EDIT HANDLER
    
    def make_edit_handler(self, row_data):

        def handler():
            self.edit_transaction(row_data)

        return handler


    # DELETE
    
    def delete_transaction(self, transaction_id):

        reply = QMessageBox.question(
            self,
            "Delete",
            "Are you sure?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            database.delete_transaction(transaction_id)
            refresh_manager.data_changed.emit()


    # EDIT
    
    def edit_transaction(self, transaction):

        dialog = EditTransactionDialog(transaction)

        if dialog.exec():
            self.load_transactions()