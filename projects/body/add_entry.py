from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDateEdit
from PySide6.QtCore import QDate, Signal
from PySide6.QtGui import QDoubleValidator
import database


class AddEntryPage(QWidget):
    entry_added = Signal()  

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(QLabel("Date:"))
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.layout.addWidget(self.date_input)

        validator = QDoubleValidator(0.0, 500.0, 2)

        self.weight = self.create_input("Weight (kg)", validator)
        self.waist = self.create_input("Waist (cm)", validator)
        self.chest = self.create_input("Chest (cm)", validator)
        self.arms = self.create_input("Arms (cm)", validator)

        btn = QPushButton("Save Entry")
        btn.clicked.connect(self.save_entry)
        self.layout.addWidget(btn)

    def create_input(self, label, validator):
        self.layout.addWidget(QLabel(label))
        field = QLineEdit()
        field.setValidator(validator)
        self.layout.addWidget(field)
        return field

    def save_entry(self):
        if not self.weight.text():
            QMessageBox.warning(self, "Error", "Weight is required")
            return

        height = database.get_user_height()

        
        if height <= 0:
            QMessageBox.warning(self, "Error", "Please set your height in Settings first")
            return

        database.add_weight_entry(
            self.date_input.date().toString("yyyy-MM-dd"),
            float(self.weight.text()),
            float(self.waist.text() or 0),
            float(self.chest.text() or 0),
            float(self.arms.text() or 0)
        )

        QMessageBox.information(self, "Success", "Entry saved!")

        # Trigger dashboard update
        self.entry_added.emit()

        # Clear fields
        self.weight.clear()
        self.waist.clear()
        self.chest.clear()
        self.arms.clear()