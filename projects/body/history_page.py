from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QAbstractItemView
import database
from PySide6.QtCore import Qt

class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        # 1. Initialize Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Weight (kg)", "Waist (cm)", "Chest (cm)", "Arms (cm)", "BMI"])
        
        # Hide ID column but keep data accessible for deletion
        self.table.setColumnHidden(0, True)

        # 2. THE FIX: Make the table take up all available space
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch) # This stretches columns to fit the window
        
        # Better selection behavior
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows) # Select whole row, not just one cell
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers) # Make it read-only
        
        # 3. Styling the table to match the "Juicy" theme
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

        # Delete Button Styling
        self.del_btn = QPushButton("Delete Selected Entry")
        self.del_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.del_btn.clicked.connect(self.delete)
        self.layout.addWidget(self.del_btn)

        self.load_data()

    def showEvent(self, event):
        """Auto-refresh the table whenever you switch to this page"""
        self.load_data()
        super().showEvent(event)

    def load_data(self):
        # NOTE: Ensure your database.get_all_history() uses "ORDER BY id DESC" or "ORDER BY date DESC"
        data = database.get_all_history()
        self.table.setRowCount(0)

        for row_idx, entry in enumerate(data):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(entry):
                item = QTableWidgetItem(str(value))
                # Center the text in the cells
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

    def delete(self):
        row = self.table.currentRow()
        if row < 0:
            return

        entry_id = int(self.table.item(row, 0).text())
        database.delete_entry(entry_id)
        self.load_data()