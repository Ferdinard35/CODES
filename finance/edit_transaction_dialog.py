from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QComboBox,
    QDateEdit,
    QMessageBox
)

from PySide6.QtCore import QDate
import database


class EditTransactionDialog(QDialog):

    def __init__(self, transaction):
        super().__init__()

        self.transaction = transaction
        self.setWindowTitle("Edit Transaction")
        self.setMinimumWidth(300)

        layout = QVBoxLayout(self)

        # DATA UNPACK
        self.transaction_id = transaction[0]

        date_val = transaction[1]
        category_val = transaction[2]
        description_val = transaction[3]
        amount_val = transaction[4] / 100
        type_val = transaction[5]

        # DATE
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.fromString(date_val, "yyyy-MM-dd"))

        # CATEGORY
        self.category_input = QLineEdit()
        self.category_input.setText(category_val)

        # DESCRIPTION
        self.desc_input = QLineEdit()
        self.desc_input.setText(description_val)

        # AMOUNT
        self.amount_input = QLineEdit()
        self.amount_input.setText(str(amount_val))

        # TYPE
        self.type_input = QComboBox()
        self.type_input.addItems(["Income", "Expense"])
        self.type_input.setCurrentText(type_val)

        # SAVE BUTTON
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.clicked.connect(self.save_changes)

        # ADD TO LAYOUT
        layout.addWidget(QLabel("Date"))
        layout.addWidget(self.date_edit)

        layout.addWidget(QLabel("Category"))
        layout.addWidget(self.category_input)

        layout.addWidget(QLabel("Description"))
        layout.addWidget(self.desc_input)

        layout.addWidget(QLabel("Amount"))
        layout.addWidget(self.amount_input)

        layout.addWidget(QLabel("Type"))
        layout.addWidget(self.type_input)

        layout.addWidget(self.save_btn)

    def save_changes(self):

        try:
            database.update_transaction(
                self.transaction_id,
                self.date_edit.date().toString("yyyy-MM-dd"),
                self.category_input.text(),
                self.desc_input.text(),
                float(self.amount_input.text()),
                self.type_input.currentText()
            )

            QMessageBox.information(
                self,
                "Success",
                "Transaction updated successfully!"
            )

            self.accept()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )