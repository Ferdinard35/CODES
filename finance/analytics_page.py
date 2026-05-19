from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QHBoxLayout
)

from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import database
from app_styles import theme_colors
from theme_manager import ThemeManager
from refresh import refresh_manager


class AnalyticsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(36, 36, 36, 36)
        self.main_layout.setSpacing(6)

        title = QLabel("Financial Analytics")
        title.setObjectName("PageTitle")
        self.main_layout.addWidget(title)

        subtitle = QLabel("Visualize spending by category and month.")
        subtitle.setObjectName("Subtitle")
        self.main_layout.addWidget(subtitle)

        self.main_layout.addSpacing(16)

        # ── STAT CARDS ──
        stats_row = QHBoxLayout()
        stats_row.setSpacing(16)

        self.balance_card, self.balance_value = self._stat_card("Current Balance", "primary")
        self.income_card,  self.income_value  = self._stat_card("Total Income",    "success")
        self.expense_card, self.expense_value = self._stat_card("Total Expenses",  "danger")

        stats_row.addWidget(self.balance_card)
        stats_row.addWidget(self.income_card)
        stats_row.addWidget(self.expense_card)
        self.main_layout.addLayout(stats_row)

        self.main_layout.addSpacing(8)

        # ── CHARTS ──
        charts_row = QHBoxLayout()
        charts_row.setSpacing(16)

        colors = self._colors()

        # Pie chart
        self.pie_frame = QFrame()
        self.pie_frame.setObjectName("ChartCard")
        pie_layout = QVBoxLayout(self.pie_frame)
        pie_layout.setContentsMargins(20, 20, 20, 20)
        pie_layout.setSpacing(10)

        pie_title = QLabel("Expense Breakdown")
        pie_title.setObjectName("SectionTitle")
        pie_layout.addWidget(pie_title)

        self.pie_figure = Figure(facecolor=colors["surface"])
        self.pie_canvas = FigureCanvas(self.pie_figure)
        pie_layout.addWidget(self.pie_canvas)

        # Line chart
        self.line_frame = QFrame()
        self.line_frame.setObjectName("ChartCard")
        line_layout = QVBoxLayout(self.line_frame)
        line_layout.setContentsMargins(20, 20, 20, 20)
        line_layout.setSpacing(10)

        line_title = QLabel("Monthly Expenses")
        line_title.setObjectName("SectionTitle")
        line_layout.addWidget(line_title)

        self.line_figure = Figure(facecolor=colors["surface"])
        self.line_canvas = FigureCanvas(self.line_figure)
        line_layout.addWidget(self.line_canvas)

        charts_row.addWidget(self.pie_frame)
        charts_row.addWidget(self.line_frame)
        self.main_layout.addLayout(charts_row)

        self.load_charts()
        refresh_manager.data_changed.connect(self.load_charts)

    def _stat_card(self, title, accent):
        card = QFrame()
        card.setObjectName("Card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(8)

        t = QLabel(title.upper())
        t.setObjectName("MetricTitle")

        v = QLabel("GHS 0.00")
        v.setObjectName("MetricValue")
        v.setProperty("accent", accent)

        layout.addWidget(t)
        layout.addWidget(v)
        return card, v

    def load_charts(self):
        self.balance_value.setText(f"GHS {database.get_balance():,.2f}")
        self.income_value.setText(f"GHS {database.get_total_income():,.2f}")
        self.expense_value.setText(f"GHS {database.get_total_expenses():,.2f}")
        self._draw_pie()
        self._draw_line()

    def _draw_pie(self):
        c = self._colors()
        data = database.get_expenses_by_category()
        categories = [r[0] for r in data]
        amounts    = [(r[1] or 0) / 100 for r in data]

        self.pie_figure.clear()
        ax = self.pie_figure.add_subplot(111)
        ax.set_facecolor(c["surface"])
        self.pie_figure.patch.set_facecolor(c["surface"])

        if amounts:
            ax.pie(amounts, labels=categories, autopct="%1.1f%%",
                   textprops={"color": c["text"]})
        else:
            ax.text(0.5, 0.5, "No expense data", ha="center", va="center",
                    color=c["muted"], fontsize=13)

        self.pie_canvas.draw()

    def _draw_line(self):
        c = self._colors()
        data   = database.get_monthly_expenses()
        months = [r[0] for r in data]
        values = [(r[1] or 0) / 100 for r in data]

        self.line_figure.clear()
        ax = self.line_figure.add_subplot(111)
        ax.set_facecolor(c["surface"])
        self.line_figure.patch.set_facecolor(c["surface"])

        if values:
            ax.plot(months, values, marker="o", linewidth=2.5, color=c["primary"])
        else:
            ax.text(0.5, 0.5, "No monthly data", ha="center", va="center",
                    color=c["muted"], fontsize=13)

        ax.set_title("Monthly Expense Trend", color=c["text"], fontsize=13, pad=10)
        ax.set_xlabel("Month", color=c["muted"], fontsize=11)
        ax.set_ylabel("GHS", color=c["muted"], fontsize=11)
        ax.tick_params(colors=c["muted"])
        ax.grid(True, alpha=0.15, color=c["border"])
        for spine in ax.spines.values():
            spine.set_edgecolor(c["border"])

        self.line_canvas.draw()

    def _colors(self):
        theme = database.get_setting("theme", ThemeManager.DARK)
        return theme_colors(theme)

    def refresh_theme(self):
        self.load_charts()
