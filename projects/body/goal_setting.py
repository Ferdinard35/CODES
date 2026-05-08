from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtGui import QDoubleValidator
import database


class GoalSettingPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        # INPUTS
        self.weight = self.create_input("Target Weight (kg)")
        self.waist = self.create_input("Target Waist (cm)")
        self.chest = self.create_input("Target Chest (cm)")

        # BUTTON
        btn = QPushButton("Save Goals")
        btn.clicked.connect(self.save_goals)
        self.layout.addWidget(btn)

        self.refresh_goals()

    def create_input(self, label):
        self.layout.addWidget(QLabel(label))

        field = QLineEdit()
        field.setValidator(QDoubleValidator(0.0, 500.0, 2))
        field.setPlaceholderText("0.0")

        self.layout.addWidget(field)
        return field

    
    # VALIDATION FIXED
    
    def get_float(self, field, name):
        text = field.text().strip()

        if text == "":
            return None

        try:
            return float(text)
        except:
            raise ValueError(f"Invalid {name}")

    
    # SAVE GOALS (FIXED)
   
    def save_goals(self):

        try:
            weight = self.get_float(self.weight, "weight")
            waist = self.get_float(self.waist, "waist")
            chest = self.get_float(self.chest, "chest")

            if weight is None and waist is None and chest is None:
                QMessageBox.warning(self, "Error", "Please enter at least one goal value")
                return

            # fallback to 0 if partially filled
            weight = weight or 0
            waist = waist or 0
            chest = chest or 0

            database.save_goals(weight, waist, chest)

            QMessageBox.information(self, "Saved", "Goals updated successfully!")

        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

        except Exception:
            QMessageBox.warning(self, "Error", "Something went wrong while saving goals")

    
    # LOAD GOALS
  
    def refresh_goals(self):
        goals = database.get_goals()

        if goals:
            weight, waist, chest = goals

            self.weight.setText(str(weight))
            self.waist.setText(str(waist))
            self.chest.setText(str(chest))