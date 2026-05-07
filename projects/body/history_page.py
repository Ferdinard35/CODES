from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
import database


class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID","Date","Weight","Waist","Chest","Arms","BMI"])
        self.table.setColumnHidden(0, True)

        self.layout.addWidget(self.table)

        btn = QPushButton("Delete")
        btn.clicked.connect(self.delete)
        self.layout.addWidget(btn)

        self.load_data()

    def load_data(self):
        data = database.get_all_history()
        self.table.setRowCount(0)

        for row, entry in enumerate(data):
            self.table.insertRow(row)
            for col, value in enumerate(entry):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def delete(self):
        row = self.table.currentRow()
        if row < 0:
            return

        entry_id = int(self.table.item(row, 0).text())

        database.delete_entry(entry_id)
        self.load_data()