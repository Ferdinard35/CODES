import sys
from PySide6.QtWidgets import  QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import database


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Body Transformation Dashboard")
        self.setMinimumSize(400, 500)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(20)

        # 1. Welcome Header
        self.welcome_label = QLabel("Welcome Back!")
        self.welcome_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.welcome_label)

        # 2. Stats Frame
        self.stats_frame = QFrame()
        self.stats_layout = QVBoxLayout(self.stats_frame)

        self.weight_display = QLabel("-- kg")
        self.weight_display.setFont(QFont("Arial", 40, QFont.Bold))
        self.weight_display.setAlignment(Qt.AlignCenter)
        self.weight_display.setStyleSheet("color: #2E86C1;")

        self.bmi_label = QLabel("BMI: --")
        self.bmi_label.setAlignment(Qt.AlignCenter)

        self.status_label = QLabel("Status: Unknown")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.stats_layout.addWidget(QLabel("Current Weight:"))
        self.stats_layout.addWidget(self.weight_display)
        self.stats_layout.addWidget(self.bmi_label)
        self.stats_layout.addWidget(self.status_label)

        self.main_layout.addWidget(self.stats_frame)

        # 3. Measurements
        self.measure_label = QLabel("Latest Measurements:")
        self.main_layout.addWidget(self.measure_label)

        self.measure_info = QLabel("Waist: -- | Chest: -- | Arms: --")
        self.measure_info.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.measure_info)

        self.refresh_dashboard()

    def get_bmi_status(self, bmi):
        if bmi < 18.5:
            return "Underweight", "#E67E22"
        elif bmi < 25:
            return "Normal", "#27AE60"
        elif bmi < 30:
            return "Overweight", "#F1C40F"
        else:
            return "Obese", "#C0392B"

    def refresh_dashboard(self):
        latest = database.get_latest_entry()
        goals = database.get_goals()
        user = database.get_user_profile()

        # Welcome name
        if user:
            self.welcome_label.setText(f"Welcome Back, {user[0]}!")

        # No data case
        if not latest:
            self.weight_display.setText("No data")
            self.bmi_label.setText("BMI: --")
            self.status_label.setText("Add your first entry")
            self.measure_info.setText("--")
            return

        weight = latest[2]
        bmi = latest[6]

        # Display values
        self.weight_display.setText(f"{weight} kg")
        self.bmi_label.setText(f"BMI: {bmi}")

        # Measurements
        self.measure_info.setText(
            f"Waist: {latest[3]} | Chest: {latest[4]} | Arms: {latest[5]}"
        )

        # Safe BMI handling
        try:
            bmi_val = float(bmi)
        except:
            bmi_val = 0

        category, color = self.get_bmi_status(bmi_val)
        self.status_label.setText(f"Status: {category}")
        self.status_label.setStyleSheet(f"color: {color};")

        # Progress logic
        if goals and goals[0]:
            diff = round(weight - goals[0], 2)

            if diff > 0:
                self.measure_label.setText(f"Progress: {diff} kg to go!")
            else:
                self.measure_label.setText("Goal reached")

    def showEvent(self, event):
        self.refresh_dashboard()
        super().showEvent(event)


