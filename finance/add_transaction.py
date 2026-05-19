from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QComboBox,
    QDateEdit,
    QTextEdit,
    QFrame,
    QSizePolicy
)

from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QFont, QDoubleValidator

import database


class AddTransactionPage(QWidget):

    def __init__(self):
        super().__init__()

        self._transaction_type = "Income"

        # MAIN LAYOUT
        outer = QVBoxLayout(self)
        outer.setContentsMargins(36, 36, 36, 36)
        outer.setSpacing(6)

        # TITLE
        title = QLabel("Add Transaction")
        title.setObjectName("PageTitle")
        outer.addWidget(title)

        subtitle = QLabel("Record income and expenses with a date, category, and description.")
        subtitle.setObjectName("Subtitle")
        outer.addWidget(subtitle)

        outer.addSpacing(12)

        # FORM CARD
        self.form_card = QFrame()
        self.form_card.setObjectName("FormCard")
        self.form_card.setMaximumWidth(780)

        form = QVBoxLayout(self.form_card)
        form.setContentsMargins(28, 28, 28, 28)
        form.setSpacing(18)

        # ── ROW 1: Date + Category ──
        row1 = QHBoxLayout()
        row1.setSpacing(16)

        date_col = QVBoxLayout()
        date_col.setSpacing(6)
        date_col.addWidget(self._field_label("Date"))
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setMinimumHeight(42)
        date_col.addWidget(self.date_input)

        cat_col = QVBoxLayout()
        cat_col.setSpacing(6)
        cat_col.addWidget(self._field_label("Category"))
        self.category_input = QComboBox()
        self.category_input.addItems([
            "Food", "Transport", "Shopping", "Bills",
            "Entertainment", "Salary", "Investment",
            "Health", "Education", "Other"
        ])
        self.category_input.setMinimumHeight(42)
        cat_col.addWidget(self.category_input)

        row1.addLayout(date_col)
        row1.addLayout(cat_col)
        form.addLayout(row1)

        # ── DESCRIPTION ──
        desc_col = QVBoxLayout()
        desc_col.setSpacing(6)
        desc_col.addWidget(self._field_label("Description"))
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter transaction description...")
        self.description_input.setFixedHeight(80)
        desc_col.addWidget(self.description_input)
        form.addLayout(desc_col)

        # ── ROW 2: Amount + Type ──
        row2 = QHBoxLayout()
        row2.setSpacing(16)

        amt_col = QVBoxLayout()
        amt_col.setSpacing(6)
        amt_col.addWidget(self._field_label("Amount (GHS)"))
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        self.amount_input.setMinimumHeight(42)
        validator = QDoubleValidator(0.00, 999999999.99, 2)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.amount_input.setValidator(validator)
        amt_col.addWidget(self.amount_input)

        type_col = QVBoxLayout()
        type_col.setSpacing(6)
        type_col.addWidget(self._field_label("Transaction Type"))

        # Toggle buttons
        toggle_frame = QFrame()
        toggle_frame.setObjectName("FormCard")
        toggle_frame.setStyleSheet(
            "QFrame#FormCard { border-radius: 8px; padding: 3px; }"
        )
        toggle_layout = QHBoxLayout(toggle_frame)
        toggle_layout.setContentsMargins(4, 4, 4, 4)
        toggle_layout.setSpacing(4)

        self.income_btn = QPushButton("Income")
        self.income_btn.setObjectName("ToggleIncomeActive")
        self.income_btn.setMinimumHeight(34)
        self.income_btn.setCursor(Qt.PointingHandCursor)
        self.income_btn.clicked.connect(lambda: self._set_type("Income"))

        self.expense_btn = QPushButton("Expense")
        self.expense_btn.setObjectName("ToggleInactive")
        self.expense_btn.setMinimumHeight(34)
        self.expense_btn.setCursor(Qt.PointingHandCursor)
        self.expense_btn.clicked.connect(lambda: self._set_type("Expense"))

        toggle_layout.addWidget(self.income_btn)
        toggle_layout.addWidget(self.expense_btn)

        type_col.addWidget(toggle_frame)

        row2.addLayout(amt_col)
        row2.addLayout(type_col)
        form.addLayout(row2)

        # ── SUBMIT ──
        self.add_button = QPushButton("Add Transaction")
        self.add_button.setMinimumHeight(46)
        self.add_button.setCursor(Qt.PointingHandCursor)
        self.add_button.clicked.connect(self.add_transaction)
        form.addWidget(self.add_button)

        card_row = QHBoxLayout()
        card_row.addWidget(self.form_card)
        card_row.addStretch()
        outer.addLayout(card_row)
        outer.addStretch()

    def _field_label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("FieldLabel")
        return lbl

    def _set_type(self, t):
        self._transaction_type = t
        if t == "Income":
            self.income_btn.setObjectName("ToggleIncomeActive")
            self.expense_btn.setObjectName("ToggleInactive")
        else:
            self.income_btn.setObjectName("ToggleInactive")
            self.expense_btn.setObjectName("ToggleExpenseActive")
        for btn in [self.income_btn, self.expense_btn]:
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    # ── ADD TRANSACTION ──
    def add_transaction(self):
        date = self.date_input.date().toString("yyyy-MM-dd")
        category = self.category_input.currentText()
        description = self.description_input.toPlainText().strip()
        amount_text = self.amount_input.text().strip()
        trans_type = self._transaction_type

        if not amount_text:
            QMessageBox.warning(self, "Error", "Please enter an amount.")
            return
        if not description:
            QMessageBox.warning(self, "Error", "Please enter a description.")
            return
        try:
            amount = float(amount_text)
            if amount <= 0:
                QMessageBox.warning(self, "Error", "Amount must be greater than 0.")
                return
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid amount entered.")
            return

        database.add_transaction(date, category, description, amount, trans_type)
        QMessageBox.information(self, "Success", "Transaction added successfully!")

        self.description_input.clear()
        self.amount_input.clear()
        self.category_input.setCurrentIndex(0)
        self._set_type("Income")
        self.date_input.setDate(QDate.currentDate())
