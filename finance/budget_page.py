from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QProgressBar,
    QMessageBox,
    QFrame
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from datetime import datetime

import database


class BudgetPage(QWidget):

    def __init__(self):
        super().__init__()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(36, 36, 36, 36)
        outer.setSpacing(6)

        # TITLE
        title = QLabel("Budget Tracking")
        title.setObjectName("PageTitle")
        outer.addWidget(title)

        subtitle = QLabel("Set a monthly spending target and track progress against expenses.")
        subtitle.setObjectName("Subtitle")
        outer.addWidget(subtitle)

        outer.addSpacing(16)

        # ── METRIC CARDS ──
        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)

        self.budget_card,    self.budget_val    = self._metric_card("Monthly Budget")
        self.spent_card,     self.spent_val     = self._metric_card("Spent This Month")
        self.remaining_card, self.remaining_val = self._metric_card("Remaining")

        cards_row.addWidget(self.budget_card)
        cards_row.addWidget(self.spent_card)
        cards_row.addWidget(self.remaining_card)
        outer.addLayout(cards_row)

        outer.addSpacing(8)

        # ── BUDGET FORM CARD ──
        self.card = QFrame()
        self.card.setObjectName("FormCard")
        self.card.setMaximumWidth(720)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(28, 28, 28, 28)
        card_layout.setSpacing(16)

        card_layout.addWidget(self._field_label("Monthly Budget (GHS)"))

        # Input + button row
        input_row = QHBoxLayout()
        input_row.setSpacing(12)

        self.budget_input = QLineEdit()
        self.budget_input.setPlaceholderText("Enter monthly budget amount...")
        self.budget_input.setMinimumHeight(42)

        self.save_btn = QPushButton("Save Budget")
        self.save_btn.setMinimumHeight(42)
        self.save_btn.setMinimumWidth(140)
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_budget)

        input_row.addWidget(self.budget_input)
        input_row.addWidget(self.save_btn)
        card_layout.addLayout(input_row)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.progress.setMinimumHeight(10)
        self.progress.setMaximumHeight(10)
        self.progress.setTextVisible(False)
        card_layout.addWidget(self.progress)

        # Progress labels row
        prog_row = QHBoxLayout()
        self.progress_pct = QLabel("0% used")
        self.progress_pct.setObjectName("Subtitle")

        self.status = QLabel("")
        self.status.setObjectName("StatusLabel")
        self.status.setAlignment(Qt.AlignRight)

        prog_row.addWidget(self.progress_pct)
        prog_row.addStretch()
        prog_row.addWidget(self.status)
        card_layout.addLayout(prog_row)

        card_row = QHBoxLayout()
        card_row.addWidget(self.card)
        card_row.addStretch()
        outer.addLayout(card_row)
        outer.addStretch()

        self.load_budget()

    def _field_label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("FieldLabel")
        return lbl

    def _metric_card(self, title):
        card = QFrame()
        card.setObjectName("Card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(8)

        t = QLabel(title.upper())
        t.setObjectName("MetricTitle")

        v = QLabel("—")
        v.setObjectName("MetricValue")

        layout.addWidget(t)
        layout.addWidget(v)
        return card, v

    def save_budget(self):
        text = self.budget_input.text().strip()

        if not text:
            QMessageBox.warning(self, "Error", "Please enter a budget amount.")
            return
        try:
            amount = float(text)
            if amount <= 0:
                QMessageBox.warning(self, "Error", "Budget must be greater than 0.")
                return
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid amount entered.")
            return

        month = datetime.now().strftime("%Y-%m")
        database.set_budget(month, amount)
        QMessageBox.information(self, "Saved", "Budget updated successfully.")
        self.budget_input.clear()
        self.load_budget()

    def load_budget(self):
        month = datetime.now().strftime("%Y-%m")
        budget_cents = database.get_budget(month)
        spent_cents  = database.get_month_expenses(month)

        budget = (budget_cents or 0) / 100
        spent  = (spent_cents  or 0) / 100

        # Update metric cards
        self.budget_val.setText(f"GHS {budget:,.2f}" if budget > 0 else "—")
        self.budget_val.setStyleSheet("")

        self.spent_val.setText(f"GHS {spent:,.2f}")
        self.spent_val.setStyleSheet("color: #ef4444;")

        if budget > 0:
            remaining = budget - spent
            color = "#22c55e" if remaining >= 0 else "#ef4444"
            self.remaining_val.setText(f"GHS {remaining:,.2f}")
            self.remaining_val.setStyleSheet(f"color: {color};")
        else:
            self.remaining_val.setText("—")
            self.remaining_val.setStyleSheet("")

        # Progress
        if budget > 0:
            percent = (spent / budget) * 100
        else:
            percent = 0

        percent_int = min(int(percent), 100)
        self.progress.setValue(percent_int)
        self.progress_pct.setText(f"{percent_int}% used")

        # Color the progress bar chunk
        if percent > 100:
            chunk_color = "#ef4444"
        elif percent > 80:
            chunk_color = "#f59e0b"
        else:
            chunk_color = "#3b82f6"

        self.progress.setStyleSheet(
            f"QProgressBar::chunk {{ background-color: {chunk_color}; border-radius: 6px; }}"
        )

        # Status label
        if budget <= 0:
            self.status.setText("No budget set for this month")
            self._set_status("warning")
        elif percent > 100:
            over = spent - budget
            self.status.setText(f"Over budget by GHS {over:,.2f}")
            self._set_status("danger")
        else:
            remaining = budget - spent
            self.status.setText(f"GHS {remaining:,.2f} remaining")
            self._set_status("success")

    def _set_status(self, state):
        self.status.setProperty("state", state)
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)
