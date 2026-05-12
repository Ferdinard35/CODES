from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import database


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        # MAIN LAYOUT
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(50, 40, 50, 40)
        self.main_layout.setSpacing(22)

        # HEADER
        self.user_label = QLabel("👋 Welcome Back")
        self.user_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.user_label.setStyleSheet("color: white;")

        self.subtitle = QLabel("Your fitness overview at a glance")
        self.subtitle.setStyleSheet("color: #94a3b8; font-size: 14px;")

        self.main_layout.addWidget(self.user_label)
        self.main_layout.addWidget(self.subtitle)

        # MAIN CARD
        self.stats_frame = QFrame()
        self.stats_frame.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border-radius: 20px;
                border: 1px solid #1f2937;
            }
        """)

        self.stats_layout = QVBoxLayout(self.stats_frame)
        self.stats_layout.setContentsMargins(30, 25, 30, 25)
        self.stats_layout.setSpacing(18)

        # WEIGHT
        self.weight_title = QLabel("Current Weight")
        self.weight_title.setStyleSheet("color: #94a3b8; font-size: 13px;")

        self.weight_display = QLabel("-- kg")
        self.weight_display.setFont(QFont("Segoe UI", 36, QFont.Bold))
        self.weight_display.setStyleSheet("color: #60a5fa;")

        self.stats_layout.addWidget(self.weight_title)
        self.stats_layout.addWidget(self.weight_display)

        # BMI
        self.bmi_label = QLabel("BMI: --")
        self.bmi_label.setStyleSheet("color: #cbd5e1; font-size: 14px;")
        self.stats_layout.addWidget(self.bmi_label)

        # STATUS
        self.status_label = QLabel("Status: --")
        self.status_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.stats_layout.addWidget(self.status_label)

        # GOAL
        self.goal_card = QFrame()
        self.goal_card.setStyleSheet("""
            QFrame {
                background-color: #0f172a;
                border-radius: 16px;
                border: 1px solid #1f2937;
            }
        """)

        self.goal_layout = QVBoxLayout(self.goal_card)
        self.goal_layout.setContentsMargins(18, 14, 18, 14)
        self.goal_layout.setSpacing(6)

        self.goal_title = QLabel("Goal")
        self.goal_title.setStyleSheet("color: #94a3b8; font-size: 13px; font-weight: bold;")

        self.goal_value = QLabel("Not set")
        self.goal_value.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.goal_value.setStyleSheet("color: #cbd5e1;")

        self.goal_layout.addWidget(self.goal_title)
        self.goal_layout.addWidget(self.goal_value)

        self.stats_layout.addWidget(self.goal_card)

        # MEASUREMENTS
        self.measure_card = QFrame()
        self.measure_card.setStyleSheet("""
            QFrame {
                background-color: #0f172a;
                border-radius: 16px;
                border: 1px solid #1f2937;
            }
        """)

        self.measure_layout = QVBoxLayout(self.measure_card)
        self.measure_layout.setContentsMargins(18, 18, 18, 18)

        self.measure_label = QLabel("Latest Measurements")
        self.measure_label.setStyleSheet("color: white; font-weight: bold;")

        self.measure_info = QLabel("Waist: -- | Chest: -- | Arms: --")
        self.measure_info.setStyleSheet("color: #cbd5e1; font-size: 13px;")

        self.measure_layout.addWidget(self.measure_label)
        self.measure_layout.addWidget(self.measure_info)

        # ADD TO UI
        self.main_layout.addWidget(self.stats_frame)
        self.main_layout.addWidget(self.measure_card)
        self.main_layout.addStretch()

        self.refresh_dashboard()

    #BMI FUNCTION 
    def get_bmi_status(self, bmi):

        if bmi < 18.5:
            return "Underweight", "#60a5fa"

        elif 18.5 <= bmi < 25:
            return "Healthy Weight", "#22c55e"

        elif 25 <= bmi < 30:
            return "Overweight", "#facc15"

        elif 30 <= bmi < 35:
            return "Obese (Class I)", "#f97316"

        else:
            return "Severely Obese (Class II+)", "#ef4444"

    # NAME SAFE
    def get_user_name(self, profile):

        if isinstance(profile, dict):
            return profile.get("name")
        if isinstance(profile, (list, tuple)) and profile:
            return profile[0]
        return None

    # REFRESH
    def refresh_dashboard(self):

        latest = database.get_latest_entry()
        goal = database.get_current_goal()
        measurements = database.get_latest_measurements()
        profile = database.get_user_profile()

        # USER NAME
        name = self.get_user_name(profile)
        self.user_label.setText(f"👋 Welcome Back, {name}" if name else "👋 Welcome Back")

        # NO DATA
        if not latest:
            self.weight_display.setText("-- kg")
            self.bmi_label.setText("BMI: --")
            self.status_label.setText("Status: No data yet")
            self.goal_value.setText("Not set")
            self.measure_info.setText("Waist: -- | Chest: -- | Arms: --")
            return

        current_weight, bmi = latest

        self.weight_display.setText(f"{current_weight} kg")
        self.bmi_label.setText(f"BMI: {bmi}")

        status, color = self.get_bmi_status(float(bmi))
        self.status_label.setText(f"Status: {status}")
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold;")

        # GOAL
        goal_value = None

        if isinstance(goal, dict):
            goal_value = goal.get("target_weight")
        elif isinstance(goal, (list, tuple)) and goal:
            goal_value = goal[0]

        try:
            if goal_value not in [None, ""]:

                target = float(goal_value)
                current = float(current_weight)

                self.goal_value.setText(f"{target} kg")

                if current <= target:
                    self.goal_value.setStyleSheet("color: #22c55e; font-weight: bold;")
                else:
                    self.goal_value.setStyleSheet("color: #facc15; font-weight: bold;")

            else:
                self.goal_value.setText("Not set")
                self.goal_value.setStyleSheet("color: #94a3b8;")

        except:
            self.goal_value.setText("Not set")
            self.goal_value.setStyleSheet("color: #94a3b8;")

        # MEASUREMENTS
        if measurements and len(measurements) >= 3:
            waist, chest, arms = measurements[:3]
            self.measure_info.setText(
                f"Waist: {waist} cm | Chest: {chest} cm | Arms: {arms} cm"
            )

    def showEvent(self, event):
        self.refresh_dashboard()
        super().showEvent(event)