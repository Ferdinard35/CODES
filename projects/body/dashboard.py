from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

import database


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        
        # MAIN LAYOUT
       

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(40, 40, 40, 40)

        self.main_layout.setSpacing(20)

        
        # TITLE
        

        self.welcome_label = QLabel("👋 Welcome Back")

        self.welcome_label.setFont(
            QFont("Segoe UI", 22, QFont.Bold)
        )

        self.welcome_label.setStyleSheet("""
            color: white;
        """)

        self.main_layout.addWidget(self.welcome_label)

        self.subtitle = QLabel(
            "Here is your fitness summary"
        )

        self.subtitle.setStyleSheet("""
            color: #94a3b8;
            font-size: 14px;
        """)

        self.main_layout.addWidget(self.subtitle)

       
        # MAIN CARD
       

        self.stats_frame = QFrame()

        self.stats_frame.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border-radius: 22px;
                border: 1px solid #1f2937;
            }
        """)

        self.stats_layout = QVBoxLayout(self.stats_frame)

        self.stats_layout.setContentsMargins(30, 30, 30, 30)

        self.stats_layout.setSpacing(18)

        
        # WEIGHT

        self.weight_title = QLabel("Current Weight")

        self.weight_title.setStyleSheet("""
            color: #94a3b8;
            font-size: 13px;
        """)

        self.weight_display = QLabel("-- kg")

        self.weight_display.setFont(
            QFont("Segoe UI", 40, QFont.Bold)
        )

        self.weight_display.setStyleSheet("""
            color: #60a5fa;
        """)

        self.stats_layout.addWidget(self.weight_title)

        self.stats_layout.addWidget(self.weight_display)

        
        # BMI
       

        self.bmi_label = QLabel("BMI: --")

        self.bmi_label.setStyleSheet("""
            color: #cbd5e1;
            font-size: 14px;
        """)

        self.stats_layout.addWidget(self.bmi_label)

        
        # STATUS
        

        self.status_label = QLabel("Status: --")

        self.status_label.setFont(
            QFont("Segoe UI", 14, QFont.Bold)
        )

        self.stats_layout.addWidget(self.status_label)

        
        # GOAL
        

        self.goal_label = QLabel("Goal: Not set")

        self.goal_label.setStyleSheet("""
            color: #94a3b8;
            font-size: 13px;
        """)

        self.stats_layout.addWidget(self.goal_label)

        # MEASUREMENTS CARD
        

        self.measure_card = QFrame()

        self.measure_card.setStyleSheet("""
            QFrame {
                background-color: #0f172a;
                border-radius: 18px;
                border: 1px solid #1f2937;
            }
        """)

        self.measure_layout = QVBoxLayout(self.measure_card)

        self.measure_layout.setContentsMargins(20, 20, 20, 20)

        self.measure_label = QLabel("📏 Latest Measurements")

        self.measure_label.setStyleSheet("""
            color: white;
            font-weight: bold;
        """)

        self.measure_info = QLabel(
            "Waist: -- | Chest: -- | Arms: --"
        )

        self.measure_info.setStyleSheet("""
            color: #cbd5e1;
            font-size: 13px;
        """)

        self.measure_layout.addWidget(self.measure_label)

        self.measure_layout.addWidget(self.measure_info)

        
        # ADD TO LAYOUT
        

        self.main_layout.addWidget(self.stats_frame)

        self.main_layout.addWidget(self.measure_card)

        self.main_layout.addStretch()

        # LOAD DATA
        self.refresh_dashboard()

   
    # BMI STATUS
    

    def get_bmi_status(self, bmi):

        if bmi < 18.5:
            return "Underweight", "#60a5fa"

        elif bmi < 25:
            return "Normal", "#22c55e"

        elif bmi < 30:
            return "Overweight", "#facc15"

        else:
            return "Obese", "#ef4444"

    
    # REFRESH DASHBOARD
    

    def refresh_dashboard(self):

        latest = database.get_latest_entry()

        target = database.get_current_goal()

        measurements = database.get_latest_measurements()

        if not latest:

            self.weight_display.setText("-- kg")

            self.bmi_label.setText("BMI: --")

            self.status_label.setText("Status: No data yet")

            self.goal_label.setText("Goal: Not set")

            self.measure_info.setText(
                "Waist: -- | Chest: -- | Arms: --"
            )

            return

        try:

            current_weight, bmi = latest

            self.weight_display.setText(
                f"{current_weight} kg"
            )

            self.bmi_label.setText(
                f"BMI: {bmi}"
            )

            status, color = self.get_bmi_status(
                float(bmi)
            )

            self.status_label.setText(
                f"Status: {status}"
            )

            self.status_label.setStyleSheet(
                f"color: {color}; font-weight: bold;"
            )

        except:

            self.status_label.setText("Status: Error")

        
        # GOAL
       

        try:

            if target:

                target_val = float(target)

                weight_val = float(current_weight)

                if weight_val <= target_val:

                    self.goal_label.setText(
                        "🎉 Goal Achieved!"
                    )

                    self.goal_label.setStyleSheet("""
                        color: #22c55e;
                        font-weight: bold;
                    """)

                else:

                    remaining = round(
                        weight_val - target_val,
                        1
                    )

                    self.goal_label.setText(
                        f"Target: {target_val} kg | Remaining: {remaining} kg"
                    )

        except:
            self.goal_label.setText("Goal error")


        # MEASUREMENTS
       

        if measurements and len(measurements) >= 3:

            try:

                waist, chest, arms = measurements[:3]

                self.measure_info.setText(
                    f"Waist: {waist} cm | Chest: {chest} cm | Arms: {arms} cm"
                )

            except:

                self.measure_info.setText(
                    "Measurement error"
                )

    
    # AUTO REFRESH
    

    def showEvent(self, event):

        self.refresh_dashboard()

        super().showEvent(event)