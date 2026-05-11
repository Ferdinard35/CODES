from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFrame
)

from PySide6.QtGui import QDoubleValidator, QFont
from PySide6.QtCore import Qt

import database


class GoalSettingPage(QWidget):

    def __init__(self):
        super().__init__()

      
        # MAIN LAYOUT
        

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(40, 40, 40, 40)

        self.layout.setSpacing(25)

      
        # PAGE TITLE
      

        self.title = QLabel("🎯 Fitness Goals")

        self.title.setFont(QFont("Segoe UI", 22, QFont.Bold))

        self.title.setStyleSheet("""
            color: white;
        """)

        self.layout.addWidget(self.title)

      
        # SUBTITLE
     

        self.subtitle = QLabel(
            "Set your body measurement targets and track your progress."
        )

        self.subtitle.setStyleSheet("""
            color: #94a3b8;
            font-size: 14px;
        """)

        self.layout.addWidget(self.subtitle)

      
        # CARD CONTAINER
   

        self.card = QFrame()

        self.card.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border-radius: 22px;
                border: 1px solid #1f2937;
            }
        """)

        self.card_layout = QVBoxLayout(self.card)

        self.card_layout.setContentsMargins(30, 30, 30, 30)

        self.card_layout.setSpacing(22)

        
        # INPUTS

        self.weight = self.create_input(
            "🏋 Target Weight (kg)"
        )

        self.waist = self.create_input(
            "📏 Target Waist (cm)"
        )

        self.chest = self.create_input(
            "💪 Target Chest (cm)"
        )

        
        # SAVE BUTTON
        
        self.btn_save = QPushButton("Save Goals")

        self.btn_save.setCursor(Qt.PointingHandCursor)

        self.btn_save.setMinimumHeight(55)

        self.btn_save.clicked.connect(self.save_goals)

        self.btn_save.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 14px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #3b82f6;
            }

            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)

        self.card_layout.addWidget(self.btn_save)

        # ADD CARD TO PAGE
        self.layout.addWidget(self.card)

        self.layout.addStretch()

        # LOAD GOALS
        self.refresh_goals()

    
    # CREATE INPUT FIELD
    

    def create_input(self, label_text):

        container = QVBoxLayout()

        label = QLabel(label_text)

        label.setStyleSheet("""
            color: #e2e8f0;
            font-size: 14px;
            font-weight: 600;
        """)

        field = QLineEdit()

        field.setValidator(
            QDoubleValidator(0.0, 500.0, 2)
        )

        field.setPlaceholderText("Enter value...")

        field.setMinimumHeight(50)

        field.setStyleSheet("""
            QLineEdit {
                background-color: #1e293b;
                color: white;
                border: 2px solid transparent;
                border-radius: 14px;
                padding-left: 15px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 2px solid #2563eb;
                background-color: #243244;
            }
        """)

        container.addWidget(label)

        container.addWidget(field)

        self.card_layout.addLayout(container)

        return field

    
    # VALIDATION
    

    def get_float(self, field, name):

        text = field.text().strip()

        if text == "":
            return None

        try:
            return float(text)

        except:
            raise ValueError(f"Invalid {name}")

    
    # SAVE GOALS
    

    def save_goals(self):

        try:

            weight = self.get_float(
                self.weight,
                "weight"
            )

            waist = self.get_float(
                self.waist,
                "waist"
            )

            chest = self.get_float(
                self.chest,
                "chest"
            )

            if (
                weight is None and
                waist is None and
                chest is None
            ):

                QMessageBox.warning(
                    self,
                    "Error",
                    "Please enter at least one goal value"
                )

                return

            weight = weight or 0

            waist = waist or 0

            chest = chest or 0

            database.save_goals(
                weight,
                waist,
                chest
            )

            QMessageBox.information(
                self,
                "Saved",
                "Goals updated successfully!"
            )

        except ValueError as e:

            QMessageBox.warning(
                self,
                "Error",
                str(e)
            )

        except Exception:

            QMessageBox.warning(
                self,
                "Error",
                "Something went wrong while saving goals"
            )

    
    # LOAD GOALS
    

    def refresh_goals(self):

        goals = database.get_goals()

        if goals:

            weight, waist, chest = goals

            self.weight.setText(str(weight))

            self.waist.setText(str(waist))

            self.chest.setText(str(chest))