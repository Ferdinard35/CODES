from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import database


class GoalSettingPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.weight = self.create_input("Target Weight")
        self.waist = self.create_input("Target Waist")
        self.chest = self.create_input("Target Chest")

        btn = QPushButton("Save Goals")
        btn.clicked.connect(self.save_goals)
        self.layout.addWidget(btn)

        self.refresh_goals()

    def create_input(self, label):
        self.layout.addWidget(QLabel(label))
        field = QLineEdit()
        self.layout.addWidget(field)
        return field

    def save_goals(self):
        try:
            database.save_goals(
                float(self.weight.text()),
                float(self.waist.text() or 0),
                float(self.chest.text() or 0)
            )
            QMessageBox.information(self, "Saved", "Goals updated!")
        except:
            QMessageBox.warning(self, "Error", "Invalid input")

    def refresh_goals(self):
        goals = database.get_goals()
        if goals:
            self.weight.setText(str(goals[0]))
            self.waist.setText(str(goals[1]))
            self.chest.setText(str(goals[2]))