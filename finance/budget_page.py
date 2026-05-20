from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QProgressBar, QMessageBox, QFrame,
    QSizePolicy, QScrollArea, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from datetime import datetime
import database
from refresh import refresh_manager


class BudgetPage(QWidget):

    def __init__(self):
        super().__init__()

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
        title = QLabel("Budget Tracking")
        title.setObjectName("PageTitle")
        main.addWidget(title)
        main.addSpacing(4)

        subtitle = QLabel("Set a monthly spending target and track your expenses in real time.")
        subtitle.setObjectName("Subtitle")
        main.addWidget(subtitle)
        main.addSpacing(20)

        # ── METRIC CARDS ──
        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)

        self.budget_card,    self.budget_val    = self._metric_card("Monthly Budget",   None)
        self.spent_card,     self.spent_val     = self._metric_card("Spent This Month", "danger")
        self.remaining_card, self.remaining_val = self._metric_card("Remaining",        "success")

        cards_row.addWidget(self.budget_card)
        cards_row.addWidget(self.spent_card)
        cards_row.addWidget(self.remaining_card)
        main.addLayout(cards_row)
        main.addSpacing(20)

        # ── TWO COLUMN: Budget Form LEFT | Progress RIGHT ──
        two_col = QHBoxLayout()
        two_col.setSpacing(16)

        # Left: set budget card
        self.set_card = QFrame()
        self.set_card.setObjectName("FormCard")
        set_layout = QVBoxLayout(self.set_card)
        set_layout.setContentsMargins(24, 22, 24, 22)
        set_layout.setSpacing(14)

        set_title = QLabel("SET MONTHLY BUDGET")
        set_title.setObjectName("FieldLabel")
        set_layout.addWidget(set_title)

        self.budget_input = QLineEdit()
        self.budget_input.setPlaceholderText("Enter amount (GHS)...")
        self.budget_input.setMinimumHeight(42)
        set_layout.addWidget(self.budget_input)

        self.save_btn = QPushButton("Save Budget")
        self.save_btn.setMinimumHeight(42)
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_budget)
        set_layout.addWidget(self.save_btn)

        set_layout.addStretch()

        # Right: progress card
        self.prog_card = QFrame()
        self.prog_card.setObjectName("FormCard")
        prog_layout = QVBoxLayout(self.prog_card)
        prog_layout.setContentsMargins(24, 22, 24, 22)
        prog_layout.setSpacing(14)

        prog_title = QLabel("SPENDING PROGRESS")
        prog_title.setObjectName("FieldLabel")
        prog_layout.addWidget(prog_title)

        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.progress.setMinimumHeight(12)
        self.progress.setMaximumHeight(12)
        self.progress.setTextVisible(False)
        prog_layout.addWidget(self.progress)

        pct_row = QHBoxLayout()
        self.progress_pct = QLabel("0% used")
        self.progress_pct.setObjectName("Subtitle")
        self.status = QLabel("")
        self.status.setObjectName("StatusLabel")
        self.status.setAlignment(Qt.AlignRight)
        pct_row.addWidget(self.progress_pct)
        pct_row.addStretch()
        pct_row.addWidget(self.status)
        prog_layout.addLayout(pct_row)

        # Tips
        prog_layout.addSpacing(8)
        sep = QFrame()
        sep.setObjectName("SidebarDivider")
        prog_layout.addWidget(sep)
        prog_layout.addSpacing(8)

        self.tip_label = QLabel("")
        self.tip_label.setObjectName("Subtitle")
        self.tip_label.setWordWrap(True)
        prog_layout.addWidget(self.tip_label)
        prog_layout.addStretch()

        two_col.addWidget(self.set_card)
        two_col.addWidget(self.prog_card)
        main.addLayout(two_col)
        main.addSpacing(20)

        # ── THIS MONTH'S EXPENSES TABLE ──
        expenses_label = QLabel("This Month's Expenses")
        expenses_label.setObjectName("SectionTitle")
        main.addWidget(expenses_label)
        main.addSpacing(10)

        self.expense_table = QTableWidget()
        self.expense_table.setColumnCount(4)
        self.expense_table.setHorizontalHeaderLabels(["Date", "Category", "Description", "Amount"])
        self.expense_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        eh = self.expense_table.horizontalHeader()
        eh.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        eh.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        eh.setSectionResizeMode(2, QHeaderView.Stretch)
        eh.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.expense_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.expense_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.expense_table.verticalHeader().setVisible(False)
        self.expense_table.setAlternatingRowColors(True)
        self.expense_table.setShowGrid(False)
        self.expense_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        main.addWidget(self.expense_table)
        main.addStretch()

        self.load_budget()
        refresh_manager.data_changed.connect(self.load_budget)

    def _metric_card(self, title, accent):
        card = QFrame()
        card.setObjectName("Card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(8)

        t = QLabel(title.upper())
        t.setObjectName("MetricTitle")

        v = QLabel("—")
        v.setObjectName("MetricValue")
        if accent:
            v.setProperty("accent", accent)

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
        month        = datetime.now().strftime("%Y-%m")
        budget_cents = database.get_budget(month)
        spent_cents  = database.get_month_expenses(month)

        budget = (budget_cents or 0) / 100
        spent  = (spent_cents  or 0) / 100

        # ── Metric cards ──
        self.budget_val.setText(f"GHS {budget:,.2f}" if budget > 0 else "—")
        self.spent_val.setText(f"GHS {spent:,.2f}")

        if budget > 0:
            remaining = budget - spent
            color = "#22c55e" if remaining >= 0 else "#ef4444"
            self.remaining_val.setText(f"GHS {remaining:,.2f}")
            self.remaining_val.setStyleSheet(f"color: {color};")
        else:
            self.remaining_val.setText("—")
            self.remaining_val.setStyleSheet("")

        # ── Progress ──
        if budget > 0:
            percent = min((spent / budget) * 100, 100)
        else:
            percent = 0

        self.progress.setValue(int(percent))
        self.progress_pct.setText(f"{int(percent)}% used")

        if percent >= 100:
            chunk_color = "#ef4444"
        elif percent >= 80:
            chunk_color = "#f59e0b"
        else:
            chunk_color = "#3b82f6"

        self.progress.setStyleSheet(
            f"QProgressBar::chunk {{ background-color: {chunk_color}; border-radius: 6px; }}"
        )

        # ── Status + tip ──
        if budget <= 0:
            self._set_status("No budget set for this month", "warning")
            self.tip_label.setText("💡 Set a monthly budget above to start tracking your spending.")
        elif percent >= 100:
            over = spent - budget
            self._set_status(f"Over budget by GHS {over:,.2f}", "danger")
            self.tip_label.setText("⚠️ You've exceeded your budget. Consider reviewing your expenses.")
        elif percent >= 80:
            remaining = budget - spent
            self._set_status(f"GHS {remaining:,.2f} remaining", "warning")
            self.tip_label.setText("📊 You've used over 80% of your budget. Spend carefully.")
        else:
            remaining = budget - spent
            self._set_status(f"GHS {remaining:,.2f} remaining", "success")
            self.tip_label.setText("✅ You're on track! Keep it up.")

        # ── Load this month's expenses ──
        self._load_month_expenses(month)

    def _set_status(self, text, state):
        self.status.setText(text)
        self.status.setProperty("state", state)
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)

    def _load_month_expenses(self, month):
        """Load all expense transactions for the current month into the table."""
        with database.connect_db() as conn:
            rows = conn.execute("""
                SELECT date, category, description, amount_cents
                FROM transactions
                WHERE type='Expense'
                AND substr(date, 1, 7) = ?
                ORDER BY date DESC, rowid DESC
            """, (month,)).fetchall()

        self.expense_table.setRowCount(0)

        for row_number, row in enumerate(rows):
            self.expense_table.insertRow(row_number)
            date     = row[0]
            category = row[1]
            desc     = row[2]
            amount   = (row[3] or 0) / 100

            for col, val in enumerate([date, category, desc, f"GHS {amount:,.2f}"]):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if col == 3:
                    item.setForeground(QColor("#ef4444"))
                self.expense_table.setItem(row_number, col, item)

        # Fit height
        self.expense_table.resizeRowsToContents()
        total_h = self.expense_table.horizontalHeader().height() + 2
        for i in range(self.expense_table.rowCount()):
            total_h += self.expense_table.rowHeight(i)
        if self.expense_table.rowCount() == 0:
            total_h += 60
        self.expense_table.setFixedHeight(total_h)
