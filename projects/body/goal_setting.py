from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFrame
)

from PySide6.QtGui import QDoubleValidator, QFont
from PySide6.QtCore import Qt, Signal

import database


class GoalSettingPage(QWidget):

    # 🔥 SIGNAL ADDED (fixes your crash)
    goal_saved = Signal()

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(25)

        self.title = QLabel("🎯 Fitness Goals")
        self.title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.title.setStyleSheet("color: white;")
        self.layout.addWidget(self.title)

        self.subtitle = QLabel(
            "Set your body measurement targets and track your progress."
        )
        self.subtitle.setStyleSheet("color: #94a3b8; font-size: 14px;")
        self.layout.addWidget(self.subtitle)

        # CARD
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

        self.weight = self.create_input("🏋 Target Weight (kg)")
        self.waist = self.create_input("📏 Target Waist (cm)")
        self.chest = self.create_input("💪 Target Chest (cm)")

        self.btn_save = QPushButton("Save Goals")
        self.btn_save.setMinimumHeight(55)
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_save.clicked.connect(self.save_goals)

        self.btn_save.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border-radius: 14px;
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

        self.layout.addWidget(self.card)
        self.layout.addStretch()

        self.refresh_goals()

    def create_input(self, label_text):

        container = QVBoxLayout()

        label = QLabel(label_text)
        label.setStyleSheet("color: #e2e8f0; font-weight: 600;")

        field = QLineEdit()
        field.setValidator(QDoubleValidator(0.0, 500.0, 2))
        field.setPlaceholderText("Enter value...")
        field.setMinimumHeight(50)

        field.setStyleSheet("""
            QLineEdit {
                background-color: #1e293b;
                color: white;
                border-radius: 14px;
                padding-left: 15px;
                border: 2px solid transparent;
            }
            QLineEdit:focus {
                border: 2px solid #2563eb;
            }
        """)

        container.addWidget(label)
        container.addWidget(field)
        self.card_layout.addLayout(container)

        return field

    def to_float(self, field):
        text = field.text().strip()
        if not text:
            return None
        try:
            return float(text)
        except:
            return None

    def save_goals(self):

        weight = self.to_float(self.weight)
        waist = self.to_float(self.waist)
        chest = self.to_float(self.chest)

        if weight is None and waist is None and chest is None:
            QMessageBox.warning(self, "Error", "Enter at least one goal")
            return

        database.save_goals(
            weight or 0,
            waist or 0,
            chest or 0
        )

        # 🔥 BEAUTIFUL POPUP
        msg = QMessageBox(self)
        msg.setWindowTitle("Goals Saved")
        msg.setText("🎯 Goals updated successfully!")

        msg.setStyleSheet("""
            QMessageBox {
                background-color: #0f172a;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #22c55e;
                color: white;
                padding: 8px 16px;
                border-radius: 10px;
            }
        """)

        msg.exec()

        # 🔥 SIGNAL EMIT (this fixes your main.py crash)
        self.goal_saved.emit()

        self.refresh_goals()

    def refresh_goals(self):

        goals = database.get_goals()

        if not goals:
            return

        self.weight.setText(str(goals.get("weight") or ""))
        self.waist.setText(str(goals.get("waist") or ""))
        self.chest.setText(str(goals.get("chest") or ""))