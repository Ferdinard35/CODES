from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView,
    QAbstractItemView, QMessageBox, QLabel
)
from PySide6.QtCore import Qt
import database


class HistoryPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        # EMPTY STATE LABEL
        self.empty_label = QLabel("No history available")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("color: gray; font-size: 16px;")
        self.layout.addWidget(self.empty_label)

        # TABLE
        self.table = QTableWidget()
        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels([
            "ID", "Date", "Weight (kg)", "Waist (cm)",
            "Chest (cm)", "Arms (cm)", "BMI"
        ])
        
        self.table.setColumnHidden(0, True)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e272e;
                color: white;
                gridline-color: #34495e;
                border: none;
                border-radius: 10px;
                font-size: 14px;
            }

            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 5px;
                font-weight: bold;
                border: 1px solid #2c3e50;
            }

            QTableWidget::item:selected {
                background-color: #00FF7F;
                color: #1e272e;
            }
        """)

        self.layout.addWidget(self.table)

        # DELETE BUTTON
        self.del_btn = QPushButton("Delete Selected Entry")
        self.del_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        self.del_btn.clicked.connect(self.delete_entry)
        self.layout.addWidget(self.del_btn)

        self.load_data()

    
    # AUTO REFRESH ON OPEN
    
    def showEvent(self, event):
        self.load_data()
        super().showEvent(event)

    
    # LOAD DATA (FIXED)
    
    def load_data(self):

        data = database.get_all_history()

        self.table.setRowCount(0)

        if not data:
            self.table.hide()
            self.empty_label.show()
            return

        self.empty_label.hide()
        self.table.show()

        for row_idx, entry in enumerate(data):
            self.table.insertRow(row_idx)

            for col_idx, value in enumerate(entry):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

    
    # DELETE ENTRY (SAFE)
    
    def delete_entry(self):

        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a row first")
            return

        item = self.table.item(row, 0)

        if not item:
            return

        try:
            entry_id = int(item.text())
        except:
            QMessageBox.warning(self, "Error", "Invalid entry selected")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this entry?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            database.delete_entry(entry_id)
            self.load_data()