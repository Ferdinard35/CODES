from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import database


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Weight tracker")
        self.setMinimumSize(400, 500)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        
        # WELCOME HEADER
        
        self.welcome_label = QLabel("Welcome Back 👋")
        self.welcome_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.welcome_label)

        
        # STATS FRAME
       
        self.stats_frame = QFrame()
        self.stats_frame.setStyleSheet("""
            QFrame {
                background-color: #1e272e;
                border-radius: 15px;
                padding: 15px;
            }
        """)

        self.stats_layout = QVBoxLayout(self.stats_frame)

        self.weight_display = QLabel("-- kg")
        self.weight_display.setFont(QFont("Arial", 40, QFont.Bold))
        self.weight_display.setAlignment(Qt.AlignCenter)
        self.weight_display.setStyleSheet("color: #00FF7F;")

        self.bmi_label = QLabel("BMI: --")
        self.bmi_label.setAlignment(Qt.AlignCenter)
        self.bmi_label.setFont(QFont("Arial", 14))

        self.status_label = QLabel("Status: Unknown")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 14, QFont.Bold))

        self.goal_label = QLabel("No Goal Set")
        self.goal_label.setAlignment(Qt.AlignCenter)
        self.goal_label.setFont(QFont("Arial", 12, QFont.Bold))

        self.stats_layout.addWidget(QLabel("Current Weight:"))
        self.stats_layout.addWidget(self.weight_display)
        self.stats_layout.addWidget(self.bmi_label)
        self.stats_layout.addWidget(self.status_label)
        self.stats_layout.addWidget(self.goal_label)

        self.main_layout.addWidget(self.stats_frame)

        # MEASUREMENTS
        
        self.measure_label = QLabel("Latest Measurements")
        self.measure_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.main_layout.addWidget(self.measure_label)

        self.measure_info = QLabel("Waist: -- | Chest: -- | Arms: --")
        self.measure_info.setAlignment(Qt.AlignCenter)
        self.measure_info.setFont(QFont("Arial", 12))
        self.main_layout.addWidget(self.measure_info)

        self.refresh_dashboard()

  
    # BMI STATUS
    
    def get_bmi_status(self, bmi):
        if bmi < 18.5:
            return "Underweight", "#E67E22"
        elif bmi < 25:
            return "Normal", "#27AE60"
        elif bmi < 30:
            return "Overweight", "#F1C40F"
        else:
            return "Obese", "#C0392B"

    
    # REFRESH DASHBOARD
    def refresh_dashboard(self):

     latest = database.get_latest_entry()
     target = database.get_current_goal()
     measurements = database.get_latest_measurements()

     # RESET UI EVERY TIME (IMPORTANT FIX)
     self.status_label.setStyleSheet("")  # reset style

     if not latest:
        self.weight_display.setText("-- kg")
        self.bmi_label.setText("BMI: --")
        self.status_label.setText("No entries yet")
        self.goal_label.setText("No Goal Set")
        self.measure_info.setText("Waist: -- | Chest: -- | Arms: --")
        return

     try:
        current_weight, bmi = latest

        self.weight_display.setText(f"{current_weight} kg")
        self.bmi_label.setText(f"BMI: {bmi}")

        bmi_value = float(bmi)
        status, color = self.get_bmi_status(bmi_value)

        self.status_label.setText(f"STATUS: {status}")
        self.status_label.setStyleSheet(
            f"color: {color}; font-weight: bold; font-size: 18px;"
        )

     except Exception:
        self.status_label.setText("STATUS: Unknown")

     # GOAL
     try:
        if target is not None:
            target_val = float(target)
            weight_val = float(current_weight)

            if weight_val <= target_val:
                self.goal_label.setText("🎉 GOAL REACHED")
                self.goal_label.setStyleSheet("""
                    background-color: #27ae60;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                """)
            else:
                remaining = round(weight_val - target_val, 1)
                self.goal_label.setText(
                    f"Target: {target_val} kg | Remaining: {remaining} kg"
                )
                self.goal_label.setStyleSheet("color: #bdc3c7; font-weight: bold;")

     except Exception:
        self.goal_label.setText("Goal data error")

     # MEASUREMENTS (SAFE FIX)
     if measurements and len(measurements) >= 3:
        try:
            waist = measurements[0]
            chest = measurements[1]
            arms = measurements[2]

            self.measure_info.setText(
                f"Waist: {waist} cm | Chest: {chest} cm | Arms: {arms} cm"
            )
        except:
            self.measure_info.setText("Measurement data error")

    
    # AUTO REFRESH
    
    def showEvent(self, event):
        self.refresh_dashboard()
        super().showEvent(event)