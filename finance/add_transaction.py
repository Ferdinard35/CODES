from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QComboBox, QDateEdit,
    QTextEdit, QFrame, QSizePolicy, QScrollArea
)
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QDoubleValidator
import database


class AddTransactionPage(QWidget):

    def __init__(self):
        super().__init__()
        self._transaction_type = "Income"

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        container = QWidget()
        main = QVBoxLayout(container)
        main.setContentsMargins(36, 36, 36, 36)
        main.setSpacing(0)

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

        # TITLE
        title = QLabel("Add Transaction")
        title.setObjectName("PageTitle")
        main.addWidget(title)
        main.addSpacing(4)

        subtitle = QLabel("Record income and expenses with a date, category, and description.")
        subtitle.setObjectName("Subtitle")
        main.addWidget(subtitle)
        main.addSpacing(20)

        # FORM CARD — full width
        self.form_card = QFrame()
        self.form_card.setObjectName("FormCard")
        self.form_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        form = QVBoxLayout(self.form_card)
        form.setContentsMargins(28, 28, 28, 28)
        form.setSpacing(20)

        # ── ROW 1: Date + Category ──
        row1 = QHBoxLayout()
        row1.setSpacing(20)
        row1.addLayout(self._field_col("DATE", self._make_date()))
        row1.addLayout(self._field_col("CATEGORY", self._make_category()))
        form.addLayout(row1)

        # ── DESCRIPTION ──
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter transaction description...")
        self.description_input.setFixedHeight(90)
        form.addLayout(self._field_col("DESCRIPTION", self.description_input))

        # ── ROW 2: Amount + Type ──
        row2 = QHBoxLayout()
        row2.setSpacing(20)
        row2.addLayout(self._field_col("AMOUNT (GHS)", self._make_amount()))
        row2.addLayout(self._field_col("TRANSACTION TYPE", self._make_toggle()))
        form.addLayout(row2)

        # ── SUBMIT ──
        self.add_button = QPushButton("Add Transaction")
        self.add_button.setMinimumHeight(46)
        self.add_button.setCursor(Qt.PointingHandCursor)
        self.add_button.clicked.connect(self.add_transaction)
        form.addWidget(self.add_button)

        main.addWidget(self.form_card)
        main.addStretch()

    # ── HELPERS ──
    def _field_col(self, label_text, widget):
        col = QVBoxLayout()
        col.setSpacing(7)
        lbl = QLabel(label_text)
        lbl.setObjectName("FieldLabel")
        col.addWidget(lbl)
        col.addWidget(widget)
        return col

    def _make_date(self):
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setMinimumHeight(42)
        self.date_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return self.date_input

    def _make_category(self):
        self.category_input = QComboBox()
        self.category_input.addItems([
            "Food", "Transport", "Shopping", "Bills",
            "Entertainment", "Salary", "Investment",
            "Health", "Education", "Other"
        ])
        self.category_input.setMinimumHeight(42)
        self.category_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return self.category_input

    def _make_amount(self):
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        self.amount_input.setMinimumHeight(42)
        self.amount_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        v = QDoubleValidator(0.00, 999999999.99, 2)
        v.setNotation(QDoubleValidator.StandardNotation)
        self.amount_input.setValidator(v)
        return self.amount_input

    def _make_toggle(self):
        wrap = QFrame()
        wrap.setObjectName("ToggleWrap")
        wrap.setMinimumHeight(42)
        wrap.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        wrap.setStyleSheet("""
            QFrame#ToggleWrap {
                background-color: #111827;
                border: 1px solid #2d3f55;
                border-radius: 8px;
                padding: 3px;
            }
        """)
        layout = QHBoxLayout(wrap)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        self.income_btn = QPushButton("Income")
        self.income_btn.setObjectName("ToggleIncomeActive")
        self.income_btn.setMinimumHeight(32)
        self.income_btn.setCursor(Qt.PointingHandCursor)
        self.income_btn.clicked.connect(lambda: self._set_type("Income"))

        self.expense_btn = QPushButton("Expense")
        self.expense_btn.setObjectName("ToggleInactive")
        self.expense_btn.setMinimumHeight(32)
        self.expense_btn.setCursor(Qt.PointingHandCursor)
        self.expense_btn.clicked.connect(lambda: self._set_type("Expense"))

        layout.addWidget(self.income_btn)
        layout.addWidget(self.expense_btn)
        return wrap

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

    def add_transaction(self):
        date        = self.date_input.date().toString("yyyy-MM-dd")
        category    = self.category_input.currentText()
        description = self.description_input.toPlainText().strip()
        amount_text = self.amount_input.text().strip()
        trans_type  = self._transaction_type

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
