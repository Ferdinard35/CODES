from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QMessageBox,
    QHeaderView,
    QAbstractItemView,
    QFrame
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

import database

from refresh import refresh_manager


class HistoryPage(QWidget):

    def __init__(self):
        super().__init__()

        
        # MAIN LAYOUT
        
        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            25,
            25,
            25,
            25
        )

        self.main_layout.setSpacing(20)

    
        # TITLE
        
        self.title = QLabel(
            "Transaction History"
        )

        self.title.setFont(
            QFont(
                "Segoe UI",
                22,
                QFont.Bold
            )
        )

        self.main_layout.addWidget(
            self.title
        )

        
        # CONTAINER
        
        self.container = QFrame()

        self.container.setObjectName(
            "container"
        )

        self.container_layout = QVBoxLayout(
            self.container
        )

        self.container_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

    
        # TABLE
        self.table = QTableWidget()

        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Date",
            "Category",
            "Description",
            "Amount",
            "Type",
            "Action"
        ])

        
        # TABLE SETTINGS
    
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.setShowGrid(False)

        self.table.setMinimumHeight(500)

        self.container_layout.addWidget(
            self.table
        )

        self.main_layout.addWidget(
            self.container
        )

        
        # LOAD DATA

        self.load_transactions()

        
        # AUTO REFRESH
        
        refresh_manager.data_changed.connect(
            self.load_transactions
        )

    
        # STYLES
    
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: white;
                font-family: Segoe UI;
            }

            QLabel {
                color: white;
            }

            #container {
                background-color: #1e293b;
                border-radius: 18px;
            }

            QTableWidget {
                background-color: #1e293b;
                border: none;
                border-radius: 12px;
                gridline-color: transparent;
                font-size: 14px;
            }

            QHeaderView::section {
                background-color: #334155;
                color: white;
                border: none;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }

            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #334155;
            }

            QTableWidget::item:selected {
                background-color: #2563eb;
            }

            QPushButton {
                background-color: #dc2626;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #ef4444;
            }

            QPushButton:pressed {
                background-color: #b91c1c;
            }
        """)

    
    # LOAD TRANSACTIONS
   
    def load_transactions(self):

        transactions = (
            database.get_transactions()
        )

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(
            transactions
        ):

            self.table.insertRow(row_number)

            transaction_id = row_data[0]

            date = row_data[1]

            category = row_data[2]

            description = row_data[3]

            amount_cents = row_data[4]

            trans_type = row_data[5]

            # Convert cents to money
            amount = amount_cents / 100

            data = [
                str(transaction_id),
                date,
                category,
                description,
                f"GHS {amount:,.2f}",
                trans_type
            ]

            for column_number, data_item in enumerate(
                data
            ):

                item = QTableWidgetItem(
                    data_item
                )

                item.setTextAlignment(
                    Qt.AlignCenter
                )

                
                # COLOR CODING
                
                if column_number in [4, 5]:

                    if trans_type == "Income":

                        item.setForeground(
                            QColor("#22c55e")
                        )

                    else:

                        item.setForeground(
                            QColor("#ef4444")
                        )

                self.table.setItem(
                    row_number,
                    column_number,
                    item
                )

            
            # DELETE BUTTON
            
            delete_button = QPushButton(
                "Delete"
            )

            delete_button.clicked.connect(
                lambda checked=False,
                tid=transaction_id:
                self.delete_transaction(tid)
            )

            self.table.setCellWidget(
                row_number,
                6,
                delete_button
            )

    
    # DELETE TRANSACTION
    
    def delete_transaction(
        self,
        transaction_id
    ):

        reply = QMessageBox.question(
            self,
            "Delete Transaction",
            "Are you sure you want to delete this transaction?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:

            database.delete_transaction(
                transaction_id
            )

            QMessageBox.information(
                self,
                "Deleted",
                "Transaction deleted successfully."
            )