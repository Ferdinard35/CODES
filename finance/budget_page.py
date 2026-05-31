from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QProgressBar, QMessageBox, QFrame,
    QSizePolicy, QScrollArea, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QDialog, QDialogButtonBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QDoubleValidator
from datetime import datetime
import database
from refresh import refresh_manager


def _fit(table):
    table.resizeRowsToContents()
    h = table.horizontalHeader().height() + 2
    for i in range(table.rowCount()):
        h += table.rowHeight(i)
    if table.rowCount() == 0:
        h += 60
    table.setFixedHeight(h)


# ── Edit Budget Dialog ─────────────────────────────────────────────
class EditBudgetDialog(QDialog):
    def __init__(self, current_amount, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Monthly Budget")
        self.setMinimumWidth(340)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 28, 28, 28)
        lay.setSpacing(14)

        lbl = QLabel("MONTHLY BUDGET (GHS)")
        lbl.setObjectName("FieldLabel")
        lay.addWidget(lbl)

        self.input = QLineEdit()
        self.input.setText(str(current_amount) if current_amount > 0 else "")
        self.input.setPlaceholderText("Enter new budget amount...")
        self.input.setMinimumHeight(42)
        v = QDoubleValidator(0.01, 999999999.99, 2)
        v.setNotation(QDoubleValidator.StandardNotation)
        self.input.setValidator(v)
        lay.addWidget(self.input)

        hint = QLabel("This will replace your current budget for this month.")
        hint.setObjectName("Subtitle")
        hint.setWordWrap(True)
        lay.addWidget(hint)

        btns = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        btns.accepted.connect(self._on_save)
        btns.rejected.connect(self.reject)
        lay.addWidget(btns)

        self.new_amount = None

    def _on_save(self):
        text = self.input.text().strip()
        if not text:
            QMessageBox.warning(self, "Error", "Please enter an amount.")
            return
        try:
            val = float(text)
            if val <= 0:
                QMessageBox.warning(self, "Error", "Amount must be greater than 0.")
                return
            self.new_amount = val
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid amount.")


# ── Budget Page ────────────────────────────────────────────────────
class BudgetPage(QWidget):

    def __init__(self):
        super().__init__()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        ctr = QWidget()
        main = QVBoxLayout(ctr)
        main.setContentsMargins(36, 36, 36, 36)
        main.setSpacing(0)

        scroll.setWidget(ctr)
        outer.addWidget(scroll)

        # Title
        main.addWidget(self._lbl("Budget Tracking", "PageTitle"))
        main.addSpacing(4)
        main.addWidget(self._lbl(
            "Set a monthly spending target and track your expenses in real time.", "Subtitle"))
        main.addSpacing(20)

        # ── Metric cards ──
        cr = QHBoxLayout(); cr.setSpacing(16)
        self.budget_card,    self.budget_val    = self._metric("Monthly Budget",   None)
        self.spent_card,     self.spent_val     = self._metric("Spent This Month", "danger")
        self.remaining_card, self.remaining_val = self._metric("Remaining",        "success")
        cr.addWidget(self.budget_card)
        cr.addWidget(self.spent_card)
        cr.addWidget(self.remaining_card)
        main.addLayout(cr)
        main.addSpacing(20)

        # ── Two-column: Set Budget | Progress ──
        two = QHBoxLayout(); two.setSpacing(16)

        # Left – set / edit budget
        self.set_card = QFrame(); self.set_card.setObjectName("FormCard")
        sl = QVBoxLayout(self.set_card)
        sl.setContentsMargins(24, 22, 24, 22); sl.setSpacing(12)

        sl.addWidget(self._lbl("SET MONTHLY BUDGET", "FieldLabel"))

        self.budget_input = QLineEdit()
        self.budget_input.setPlaceholderText("Enter amount (GHS)...")
        self.budget_input.setMinimumHeight(42)
        sl.addWidget(self.budget_input)

        btn_row = QHBoxLayout(); btn_row.setSpacing(10)
        self.save_btn = QPushButton("Save Budget")
        self.save_btn.setMinimumHeight(42)
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_budget)

        self.edit_btn = QPushButton("Edit Budget")
        self.edit_btn.setObjectName("SecondaryButton")
        self.edit_btn.setMinimumHeight(42)
        self.edit_btn.setCursor(Qt.PointingHandCursor)
        self.edit_btn.clicked.connect(self.edit_budget)

        btn_row.addWidget(self.save_btn)
        btn_row.addWidget(self.edit_btn)
        sl.addLayout(btn_row)
        sl.addStretch()

        # Right – progress
        self.prog_card = QFrame(); self.prog_card.setObjectName("FormCard")
        pl = QVBoxLayout(self.prog_card)
        pl.setContentsMargins(24, 22, 24, 22); pl.setSpacing(12)

        pl.addWidget(self._lbl("SPENDING PROGRESS", "FieldLabel"))

        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.progress.setMinimumHeight(12)
        self.progress.setMaximumHeight(12)
        self.progress.setTextVisible(False)
        pl.addWidget(self.progress)

        pct_row = QHBoxLayout()
        self.pct_lbl = QLabel("0% used"); self.pct_lbl.setObjectName("Subtitle")
        self.status  = QLabel(""); self.status.setObjectName("StatusLabel")
        self.status.setAlignment(Qt.AlignRight)
        pct_row.addWidget(self.pct_lbl); pct_row.addStretch(); pct_row.addWidget(self.status)
        pl.addLayout(pct_row)

        sep = QFrame(); sep.setObjectName("SidebarDivider"); pl.addWidget(sep)

        self.tip_lbl = QLabel("")
        self.tip_lbl.setObjectName("Subtitle")
        self.tip_lbl.setWordWrap(True)
        pl.addWidget(self.tip_lbl)
        pl.addStretch()

        two.addWidget(self.set_card)
        two.addWidget(self.prog_card)
        main.addLayout(two)
        main.addSpacing(20)

        # ── This month's expenses table ──
        main.addWidget(self._lbl("This Month's Expenses", "SectionTitle"))
        main.addSpacing(10)

        self.exp_table = QTableWidget()
        self.exp_table.setColumnCount(4)
        self.exp_table.setHorizontalHeaderLabels(
            ["Date", "Category", "Description", "Amount"])
        self.exp_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        eh = self.exp_table.horizontalHeader()
        eh.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        eh.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        eh.setSectionResizeMode(2, QHeaderView.Stretch)
        eh.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.exp_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.exp_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.exp_table.verticalHeader().setVisible(False)
        self.exp_table.setAlternatingRowColors(True)
        self.exp_table.setShowGrid(False)
        self.exp_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.exp_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        main.addWidget(self.exp_table)
        main.addStretch()

        self.load_budget()
        refresh_manager.data_changed.connect(self.load_budget)

    # ── Helpers ──
    def _lbl(self, text, name):
        l = QLabel(text); l.setObjectName(name); return l

    def _metric(self, title, accent):
        card = QFrame(); card.setObjectName("Card")
        lay  = QVBoxLayout(card)
        lay.setContentsMargins(24, 20, 24, 20); lay.setSpacing(8)
        t = QLabel(title.upper()); t.setObjectName("MetricTitle")
        v = QLabel("—"); v.setObjectName("MetricValue")
        if accent:
            v.setProperty("accent", accent)
        lay.addWidget(t); lay.addWidget(v)
        return card, v

    def _set_status(self, text, state):
        self.status.setText(text)
        self.status.setProperty("state", state)
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)

    # ── Save ──
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
            QMessageBox.warning(self, "Error", "Invalid amount.")
            return

        month = datetime.now().strftime("%Y-%m")
        database.set_budget(month, amount)
        QMessageBox.information(self, "Saved", "Budget saved successfully.")
        self.budget_input.clear()
        self.load_budget()

    # ── Edit existing budget ──
    def edit_budget(self):
        month         = datetime.now().strftime("%Y-%m")
        current_cents = database.get_budget(month)
        current       = (current_cents or 0) / 100

        dlg = EditBudgetDialog(current, self)
        if dlg.exec() and dlg.new_amount is not None:
            database.set_budget(month, dlg.new_amount)
            QMessageBox.information(self, "Updated", "Budget updated successfully.")
            self.load_budget()

    # ── Load / refresh ──
    def load_budget(self):
        month        = datetime.now().strftime("%Y-%m")
        budget_cents = database.get_budget(month)
        spent_cents  = database.get_month_expenses(month)
        budget = (budget_cents or 0) / 100
        spent  = (spent_cents  or 0) / 100

        # Metric cards
        self.budget_val.setText(f"GHS {budget:,.2f}" if budget > 0 else "—")
        self.budget_val.setStyleSheet("")
        self.spent_val.setText(f"GHS {spent:,.2f}")

        if budget > 0:
            rem   = budget - spent
            color = "#22c55e" if rem >= 0 else "#ef4444"
            self.remaining_val.setText(f"GHS {rem:,.2f}")
            self.remaining_val.setStyleSheet(f"color: {color};")
        else:
            self.remaining_val.setText("—")
            self.remaining_val.setStyleSheet("")

        # Progress bar
        pct = min((spent / budget) * 100, 100) if budget > 0 else 0
        self.progress.setValue(int(pct))
        self.pct_lbl.setText(f"{int(pct)}% used")

        chunk = "#3b82f6" if pct < 80 else ("#f59e0b" if pct < 100 else "#ef4444")
        self.progress.setStyleSheet(
            f"QProgressBar::chunk {{ background-color: {chunk}; border-radius: 6px; }}")

        if budget <= 0:
            self._set_status("No budget set", "warning")
            self.tip_lbl.setText("💡 Set a monthly budget to start tracking your spending.")
        elif pct >= 100:
            over = spent - budget
            self._set_status(f"Over budget by GHS {over:,.2f}", "danger")
            self.tip_lbl.setText("⚠️ You've exceeded your budget. Review your expenses.")
        elif pct >= 80:
            self._set_status(f"GHS {budget - spent:,.2f} remaining", "warning")
            self.tip_lbl.setText("📊 Over 80% used. Spend carefully for the rest of the month.")
        else:
            self._set_status(f"GHS {budget - spent:,.2f} remaining", "success")
            self.tip_lbl.setText("✅ You're on track! Keep it up.")

        # Expense table
        with database.connect_db() as conn:
            rows = conn.execute("""
                SELECT date, category, description, amount_cents
                FROM transactions
                WHERE type='Expense' AND substr(date,1,7)=?
                ORDER BY date DESC, rowid DESC
            """, (month,)).fetchall()

        self.exp_table.setRowCount(0)
        for rn, row in enumerate(rows):
            self.exp_table.insertRow(rn)
            amount = (row[3] or 0) / 100
            for col, val in enumerate([row[0], row[1], row[2], f"GHS {amount:,.2f}"]):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if col == 3:
                    item.setForeground(QColor("#ef4444"))
                self.exp_table.setItem(rn, col, item)

        _fit(self.exp_table)
