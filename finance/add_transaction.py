from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QComboBox,
    QDateEdit,
    QTextEdit,
    QFrame
)

from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QDoubleValidator

import database


class AddTransactionPage(QWidget):

    def __init__(self):
        super().__init__()

        # MAIN LAYOUT
        
        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(40, 30, 40, 30)
        self.layout.setSpacing(18)

      
        # TITLE
       
        self.title = QLabel("Add Transaction")
        self.title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.title)

        # FORM CONTAINER
        
        self.form_container = QFrame()
        self.form_container.setObjectName("formContainer")

        self.form_layout = QVBoxLayout(self.form_container)
        self.form_layout.setSpacing(15)
        self.form_layout.setContentsMargins(25, 25, 25, 25)

        
        # DATE
        
        self.date_label = QLabel("Date")
        self.date_label.setFont(QFont("Segoe UI", 10))

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setMinimumHeight(42)

        self.form_layout.addWidget(self.date_label)
        self.form_layout.addWidget(self.date_input)

        
        # CATEGORY
        
        self.category_label = QLabel("Category")
        self.category_label.setFont(QFont("Segoe UI", 10))

        self.category_input = QComboBox()
        self.category_input.setMinimumHeight(42)

        self.category_input.addItems([
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Entertainment",
            "Salary",
            "Investment",
            "Health",
            "Education",
            "Other"
        ])

        self.form_layout.addWidget(self.category_label)
        self.form_layout.addWidget(self.category_input)

        
        # DESCRIPTION
        
        self.description_label = QLabel("Description")
        self.description_label.setFont(QFont("Segoe UI", 10))

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText(
            "Enter transaction description..."
        )
        self.description_input.setFixedHeight(90)

        self.form_layout.addWidget(self.description_label)
        self.form_layout.addWidget(self.description_input)

        
        # AMOUNT
        
        self.amount_label = QLabel("Amount (GHS)")
        self.amount_label.setFont(QFont("Segoe UI", 10))

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        self.amount_input.setMinimumHeight(42)

        validator = QDoubleValidator(0.00, 9999999.99, 2)
        validator.setNotation(QDoubleValidator.StandardNotation)

        self.amount_input.setValidator(validator)

        self.form_layout.addWidget(self.amount_label)
        self.form_layout.addWidget(self.amount_input)

        
        # TRANSACTION TYPE
       
        self.type_label = QLabel("Transaction Type")
        self.type_label.setFont(QFont("Segoe UI", 10))

        self.type_input = QComboBox()
        self.type_input.setMinimumHeight(42)

        self.type_input.addItems([
            "Income",
            "Expense"
        ])

        self.form_layout.addWidget(self.type_label)
        self.form_layout.addWidget(self.type_input)

        
        # ADD BUTTON
        
        self.add_button = QPushButton("Add Transaction")
        self.add_button.setMinimumHeight(50)

        self.add_button.clicked.connect(self.add_transaction)

        self.form_layout.addWidget(self.add_button)

        
        # ADD FORM TO MAIN LAYOUT

        self.layout.addWidget(self.form_container)

        
        # STYLES
        
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: white;
                font-family: Segoe UI;
            }

            #formContainer {
                background-color: #1e293b;
                border-radius: 18px;
            }

            QLabel {
                color: #e2e8f0;
            }

            QLineEdit,
            QTextEdit,
            QComboBox,
            QDateEdit {
                background-color: #334155;
                border: 2px solid transparent;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                color: white;
            }

            QLineEdit:focus,
            QTextEdit:focus,
            QComboBox:focus,
            QDateEdit:focus {
                border: 2px solid #3b82f6;
            }

            QPushButton {
                background-color: #2563eb;
                border: none;
                border-radius: 12px;
                color: white;
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

    
    # ADD TRANSACTION FUNCTION

    def add_transaction(self):

        date = self.date_input.date().toString("yyyy-MM-dd")

        category = self.category_input.currentText()

        description = self.description_input.toPlainText().strip()

        amount = self.amount_input.text().strip()

        trans_type = self.type_input.currentText()

        # VALIDATION
        if not amount:
            QMessageBox.warning(
                self,
                "Missing Amount",
                "Please enter an amount."
            )
            return

        try:
            amount = float(amount)

            if amount <= 0:
                QMessageBox.warning(
                    self,
                    "Invalid Amount",
                    "Amount must be greater than 0."
                )
                return

        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Please enter a valid amount."
            )
            return

        # SAVE TO DATABASE
        database.add_transaction(
            date,
            category,
            description,
            amount,
            trans_type
        )

        QMessageBox.information(
            self,
            "Success",
            "Transaction added successfully!"
        )

        # CLEAR FIELDS
        self.description_input.clear()
        self.amount_input.clear()

        self.category_input.setCurrentIndex(0)
        self.type_input.setCurrentIndex(0)

        self.date_input.setDate(QDate.currentDate())