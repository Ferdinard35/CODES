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
        self.setMinimumWidth(360)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        self.transaction_id = transaction[0]

        date_val        = transaction[1] or ""
        category_val    = transaction[2] or ""
        description_val = transaction[3] or ""
        amount_val      = (transaction[4] or 0) / 100
        type_val        = transaction[5] or "Expense"

        self.date_edit = QDateEdit()
        parsed_date = QDate.fromString(date_val, "yyyy-MM-dd")
        self.date_edit.setDate(parsed_date if parsed_date.isValid() else QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumHeight(40)

        self.category_input = QComboBox()
        self.category_input.addItems([
            "Food", "Transport", "Shopping", "Bills",
            "Entertainment", "Salary", "Investment",
            "Health", "Education", "Other"
        ])
        if self.category_input.findText(category_val) >= 0:
            self.category_input.setCurrentText(category_val)
        self.category_input.setMinimumHeight(40)

        self.desc_input = QLineEdit()
        self.desc_input.setText(description_val)
        self.desc_input.setMinimumHeight(40)

        self.amount_input = QLineEdit()
        self.amount_input.setText(str(amount_val))
        self.amount_input.setMinimumHeight(40)

        self.type_input = QComboBox()
        self.type_input.addItems(["Income", "Expense"])
        self.type_input.setCurrentText(type_val)
        self.type_input.setMinimumHeight(40)

        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setMinimumHeight(44)
        self.save_btn.setCursor(__import__("PySide6.QtCore", fromlist=["Qt"]).Qt.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_changes)

        for label_text, widget in [
            ("Date",        self.date_edit),
            ("Category",    self.category_input),
            ("Description", self.desc_input),
            ("Amount",      self.amount_input),
            ("Type",        self.type_input),
        ]:
            lbl = QLabel(label_text)
            lbl.setObjectName("FieldLabel")
            layout.addWidget(lbl)
            layout.addWidget(widget)

        layout.addSpacing(8)
        layout.addWidget(self.save_btn)

    def save_changes(self):
        description = self.desc_input.text().strip()
        amount_text = self.amount_input.text().strip()

        if not description:
            QMessageBox.warning(self, "Error", "Description cannot be empty.")
            return
        if not amount_text:
            QMessageBox.warning(self, "Error", "Amount is required.")
            return
        try:
            amount = float(amount_text)
            if amount <= 0:
                QMessageBox.warning(self, "Error", "Amount must be greater than 0.")
                return
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid amount.")
            return

        try:
            database.update_transaction(
                self.transaction_id,
                self.date_edit.date().toString("yyyy-MM-dd"),
                self.category_input.currentText(),
                description,
                amount,
                self.type_input.currentText()
            )
            QMessageBox.information(self, "Success", "Transaction updated successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
