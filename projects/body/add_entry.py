from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QDateEdit,
    QFrame
)

from PySide6.QtCore import QDate, Signal, Qt
from PySide6.QtGui import QDoubleValidator, QFont

import database


class AddEntryPage(QWidget):

    entry_added = Signal()

    def __init__(self):
        super().__init__()

        # MAIN LAYOUT
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(20)

        # TITLE
        self.title = QLabel("➕ Add New Entry")
        self.title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.title.setStyleSheet("color: white;")
        self.layout.addWidget(self.title)

        self.subtitle = QLabel("Log your body measurements")
        self.subtitle.setStyleSheet("""
            color: #94a3b8;
            font-size: 14px;
        """)
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
        self.card_layout.setSpacing(18)

        # DATE SECTION
        date_label = QLabel("📅 Date")
        date_label.setStyleSheet("color: #e2e8f0; font-weight: 600;")
        self.card_layout.addWidget(date_label)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setMinimumHeight(45)
        self.date_input.setStyleSheet("""
            QDateEdit {
                background-color: #1e293b;
                color: white;
                border-radius: 12px;
                padding: 10px;
                border: 2px solid transparent;
            }
            QDateEdit:focus {
                border: 2px solid #2563eb;
            }
        """)
        self.card_layout.addWidget(self.date_input)

        # INPUTS
        validator = QDoubleValidator(0.0, 500.0, 2)

        self.weight = self.create_input("⚖ Weight (kg)", validator)
        self.waist = self.create_input("📏 Waist (cm)", validator)
        self.chest = self.create_input("💪 Chest (cm)", validator)
        self.arms = self.create_input("💥 Arms (cm)", validator)

        # SAVE BUTTON
        self.btn = QPushButton("Save Entry")
        self.btn.setCursor(Qt.PointingHandCursor)
        self.btn.setMinimumHeight(55)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border-radius: 14px;
                font-size: 15px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #4ade80;
            }
            QPushButton:pressed {
                background-color: #16a34a;
            }
        """)

        self.btn.clicked.connect(self.save_entry)
        self.card_layout.addWidget(self.btn)

        self.layout.addWidget(self.card)
        self.layout.addStretch()

        # ENTER KEY SUPPORT
        for field in [self.weight, self.waist, self.chest, self.arms]:
            field.returnPressed.connect(self.save_entry)

    # INPUT FACTORY
    def create_input(self, label, validator):

        container = QVBoxLayout()

        lbl = QLabel(label)
        lbl.setStyleSheet("color: #e2e8f0; font-weight: 600;")

        field = QLineEdit()
        field.setValidator(validator)
        field.setPlaceholderText("0.0")
        field.setMinimumHeight(45)
        field.setStyleSheet("""
            QLineEdit {
                background-color: #1e293b;
                color: white;
                border-radius: 12px;
                padding-left: 12px;
                border: 2px solid transparent;
            }
            QLineEdit:focus {
                border: 2px solid #2563eb;
            }
        """)

        container.addWidget(lbl)
        container.addWidget(field)
        self.card_layout.addLayout(container)

        return field

    # SUCCESS POPUP (BEAUTIFIED)
    def show_success_popup(self, weight, entry_date):

        msg = QMessageBox(self)
        msg.setWindowTitle("Entry Added Successfully")
        msg.setIcon(QMessageBox.Information)

        msg.setText(f"""
            <div style="text-align:center;">
                <h2 style="color:#22c55e; margin-bottom:10px;">
                    ✔ Success!
                </h2>

                <p style="color:#e2e8f0; font-size:14px;">
                    Your entry has been saved successfully.
                </p>

                <div style="
                    margin-top:15px;
                    padding:12px;
                    background-color:#1e293b;
                    border-radius:12px;
                    border:1px solid #334155;
                ">
                    <p style="color:#94a3b8; margin:0;">
                        Weight Recorded:
                    </p>

                    <h3 style="color:white; margin:4px 0;">
                        {weight} kg
                    </h3>

                    <p style="color:#94a3b8; margin:0;">
                        Date: {entry_date}
                    </p>
                </div>
            </div>
        """)

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
                border-radius: 10px;
                padding: 8px 18px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #4ade80;
            }

            QPushButton:pressed {
                background-color: #16a34a;
            }
        """)

        msg.exec()

    # SAVE LOGIC
    def save_entry(self):

        if not self.weight.text():
            QMessageBox.warning(self, "Error", "Weight is required")
            return

        height = database.get_user_height()

        if not height:
            QMessageBox.warning(self, "Error", "Please set your height in Settings first")
            return

        date_str = self.date_input.date().toString("yyyy-MM-dd")

        if database.entry_exists(date_str):
            QMessageBox.warning(self, "Duplicate Entry", "An entry already exists for this date.")
            return

        try:
            database.add_weight_entry(
                date_str,
                float(self.weight.text()),
                float(self.waist.text() or 0),
                float(self.chest.text() or 0),
                float(self.arms.text() or 0)
            )

            self.show_success_popup(self.weight.text(), date_str)

            self.entry_added.emit()
            self.clear_fields()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    # CLEAR FORM
    def clear_fields(self):

        for field in [self.weight, self.waist, self.chest, self.arms]:
            field.clear()

        self.date_input.setDate(QDate.currentDate())