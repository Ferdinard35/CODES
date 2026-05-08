from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QDateEdit
)
from PySide6.QtCore import QDate, Signal, Qt
from PySide6.QtGui import QDoubleValidator
import database


class AddEntryPage(QWidget):

    entry_added = Signal()

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

       
        # DATE INPUT
       
        self.layout.addWidget(QLabel("Date:"))

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.layout.addWidget(self.date_input)

        
        # INPUT VALIDATOR
    
        validator = QDoubleValidator(0.0, 500.0, 2)

        self.weight = self.create_input("Weight (kg)", validator)
        self.waist = self.create_input("Waist (cm)", validator)
        self.chest = self.create_input("Chest (cm)", validator)
        self.arms = self.create_input("Arms (cm)", validator)

        
        # SAVE BUTTON

        self.btn = QPushButton("Save Entry")
        self.btn.setFixedHeight(40)
        self.btn.setCursor(Qt.PointingHandCursor)

        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        self.btn.clicked.connect(self.save_entry)
        self.layout.addWidget(self.btn)

        
        # ENTER KEY SUPPORT
        
        for field in [self.weight, self.waist, self.chest, self.arms]:
            field.returnPressed.connect(self.save_entry)

    
    # INPUT CREATOR
    
    def create_input(self, label, validator):

        self.layout.addWidget(QLabel(label))

        field = QLineEdit()
        field.setValidator(validator)
        field.setPlaceholderText("0.0")

        self.layout.addWidget(field)

        return field

    
    # SUCCESS POPUP
    
    def show_success_popup(self, weight, entry_date):

        msg = QMessageBox(self)
        msg.setWindowTitle("Entry Added")
        msg.setText("<h3>Success!</h3>")
        msg.setInformativeText(
            f"Added <b>{weight} kg</b> for <b>{entry_date}</b>."
        )
        msg.setIcon(QMessageBox.Information)
        msg.exec()

   
    # SAVE ENTRY LOGIC
   
    def save_entry(self):

        # VALIDATION
        if not self.weight.text():
            QMessageBox.warning(self, "Error", "Weight is required")
            return

        # HEIGHT CHECK
        height = database.get_user_height()
        if not height:
            QMessageBox.warning(
                self,
                "Error",
                "Please set your height in Settings first"
            )
            return

        # DATE
        date_str = self.date_input.date().toString("yyyy-MM-dd")

        # DUPLICATE CHECK
        if database.entry_exists(date_str):
            QMessageBox.warning(
                self,
                "Duplicate Entry",
                "An entry already exists for this date."
            )
            return

        # SAVE
        try:
            database.add_weight_entry(
                date_str,
                float(self.weight.text()),
                float(self.waist.text() or 0),
                float(self.chest.text() or 0),
                float(self.arms.text() or 0)
            )

            # SUCCESS FLOW
            self.show_success_popup(self.weight.text(), date_str)
            self.entry_added.emit()
            self.clear_fields()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not save entry: {str(e)}"
            )

    
    # RESET FORM
  
    def clear_fields(self):

        for field in [self.weight, self.waist, self.chest, self.arms]:
            field.clear()

        self.date_input.setDate(QDate.currentDate())