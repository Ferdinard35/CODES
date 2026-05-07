from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDateEdit
from PySide6.QtCore import QDate, Signal,Qt
from PySide6.QtGui import QDoubleValidator
import database

class AddEntryPage(QWidget):
    entry_added = Signal()  

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        # Date Input
        self.layout.addWidget(QLabel("Date:"))
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True) # Adds a nice calendar dropdown
        self.date_input.setDate(QDate.currentDate())
        self.layout.addWidget(self.date_input)

        # Validator to ensure only numbers are entered
        validator = QDoubleValidator(0.0, 500.0, 2)

        self.weight = self.create_input("Weight (kg)", validator)
        self.waist = self.create_input("Waist (cm)", validator)
        self.chest = self.create_input("Chest (cm)", validator)
        self.arms = self.create_input("Arms (cm)", validator)

        # Save Button
        btn = QPushButton("Save Entry")
        btn.setFixedHeight(40) # Makes the button a bit more prominent
        btn.clicked.connect(self.save_entry)
        self.layout.addWidget(btn)
        btn.setCursor(Qt.PointingHandCursor)
        for field in [self.weight, self.waist, self.chest, self.arms]:
         field.returnPressed.connect(self.save_entry)


    def create_input(self, label, validator):
        self.layout.addWidget(QLabel(label))
        field = QLineEdit()
        field.setValidator(validator)
        field.setPlaceholderText("0.0") # Helps the user see it's a number field
        self.layout.addWidget(field)
        return field

    def show_success_popup(self, weight, entry_date):
        """Displays a styled success message."""
        msg = QMessageBox(self)
        msg.setWindowTitle("Entry Added")
        msg.setText("<h3>Success!</h3>")
        msg.setInformativeText(f"Added <b>{weight}kg</b> to your history for <b>{entry_date}</b>.")
        msg.setIcon(QMessageBox.Information)
        # Prevents the popup from being too narrow and applies your custom styling
        msg.setStyleSheet("QLabel{ min-width: 250px; font-size: 14px; }") 
        msg.exec()

    def save_entry(self):
        # 1. Validation
        if not self.weight.text():
            QMessageBox.warning(self, "Error", "Weight is required")
            return

        # 2. Get User Height (Required for BMI calculation inside the database)
        height = database.get_user_height()
        if height <= 0:
            QMessageBox.warning(self, "Error", "Please set your height in Settings first")
            return

        # 3. Data Gathering
        # We grab the values and default to 0 if the field is empty
        w_val = self.weight.text()
        date_str = self.date_input.date().toString("yyyy-MM-dd")

        # 4. Save to Database
        try:
            database.add_weight_entry(
                date_str,
                float(w_val),
                float(self.waist.text() or 0),
                float(self.chest.text() or 0),
                float(self.arms.text() or 0)
            )

            # 5. Success Feedback
            self.show_success_popup(w_val, date_str)

            # 6. Housekeeping
            self.entry_added.emit() # Refreshes the Dashboard
            self.clear_fields()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Could not save: {str(e)}")

    def clear_fields(self):
        """Reset inputs for the next entry."""
        for field in [self.weight, self.waist, self.chest, self.arms]:
            field.clear()
        self.date_input.setDate(QDate.currentDate())