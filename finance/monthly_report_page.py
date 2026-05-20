from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea
)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import calendar
import database
from app_styles import theme_colors
from theme_manager import ThemeManager


def _month_name(ym_str):
    """Convert '2026-05' → 'May 2026'"""
    try:
        year, month = ym_str.split("-")
        return f"{calendar.month_name[int(month)]} {year}"
    except Exception:
        return ym_str


class MonthlyReportPage(QWidget):

    def __init__(self):
        super().__init__()

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        container = QWidget()
        outer = QVBoxLayout(container)
        outer.setContentsMargins(36, 36, 36, 36)
        outer.setSpacing(0)

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

        title = QLabel("Monthly Financial Reports")
        title.setObjectName("PageTitle")
        outer.addWidget(title)
        outer.addSpacing(4)

        subtitle = QLabel("Compare income, expenses, and savings across months.")
        subtitle.setObjectName("Subtitle")
        outer.addWidget(subtitle)
        outer.addSpacing(20)

        # ── SUMMARY CARDS ──
        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)

        self.best_card,  self.best_val  = self._metric_card("Best Month",          "success")
        self.worst_card, self.worst_val = self._metric_card("Worst Month",         "danger")
        self.avg_card,   self.avg_val   = self._metric_card("Avg Monthly Savings", "primary")

        cards_row.addWidget(self.best_card)
        cards_row.addWidget(self.worst_card)
        cards_row.addWidget(self.avg_card)
        outer.addLayout(cards_row)
        outer.addSpacing(20)

        # ── CHARTS ──
        charts_row = QHBoxLayout()
        charts_row.setSpacing(16)

        c = self._colors()

        self.line_frame = QFrame()
        self.line_frame.setObjectName("ChartCard")
        line_layout = QVBoxLayout(self.line_frame)
        line_layout.setContentsMargins(20, 20, 20, 20)
        line_layout.setSpacing(10)
        line_title = QLabel("Income vs Expenses")
        line_title.setObjectName("SectionTitle")
        line_layout.addWidget(line_title)
        self.line_fig = Figure(facecolor=c["surface"])
        self.line_canvas = FigureCanvas(self.line_fig)
        line_layout.addWidget(self.line_canvas)

        self.net_frame = QFrame()
        self.net_frame.setObjectName("ChartCard")
        net_layout = QVBoxLayout(self.net_frame)
        net_layout.setContentsMargins(20, 20, 20, 20)
        net_layout.setSpacing(10)
        net_title = QLabel("Net Savings Trend")
        net_title.setObjectName("SectionTitle")
        net_layout.addWidget(net_title)
        self.net_fig = Figure(facecolor=c["surface"])
        self.net_canvas = FigureCanvas(self.net_fig)
        net_layout.addWidget(self.net_canvas)

        charts_row.addWidget(self.line_frame)
        charts_row.addWidget(self.net_frame)
        outer.addLayout(charts_row)
        outer.addStretch()

        self.load_data()

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
        v.setProperty("accent", accent)

        layout.addWidget(t)
        layout.addWidget(v)
        return card, v

    def load_data(self):
        c = self._colors()
        data = database.get_monthly_summary()

        months, income, expenses, net = [], [], [], []

        for row in data:
            months.append(row[0])
            inc = (row[1] or 0) / 100
            exp = (row[2] or 0) / 100
            income.append(inc)
            expenses.append(exp)
            net.append(inc - exp)

        if net:
            best_i  = net.index(max(net))
            worst_i = net.index(min(net))
            avg     = sum(net) / len(net)

            # Use human-readable month name
            self.best_val.setText(
                f"{_month_name(months[best_i])}  +GHS {net[best_i]:,.2f}"
            )
            self.worst_val.setText(
                f"{_month_name(months[worst_i])}  GHS {net[worst_i]:,.2f}"
            )
            self.avg_val.setText(f"GHS {avg:,.2f}")
        else:
            self.best_val.setText("—")
            self.worst_val.setText("—")
            self.avg_val.setText("—")

        for v in [self.best_val, self.worst_val, self.avg_val]:
            v.style().unpolish(v)
            v.style().polish(v)

        # X-axis labels as month names
        month_labels = [_month_name(m) for m in months]

        # ── LINE CHART ──
        self.line_fig.clear()
        ax1 = self.line_fig.add_subplot(111)
        ax1.set_facecolor(c["surface"])
        self.line_fig.patch.set_facecolor(c["surface"])

        if months:
            xs = range(len(months))
            ax1.plot(xs, income,   marker="o", linewidth=2.5, color=c["success"], label="Income")
            ax1.plot(xs, expenses, marker="o", linewidth=2.5, color=c["danger"],  label="Expenses")
            ax1.set_xticks(list(xs))
            ax1.set_xticklabels(month_labels, rotation=20, ha="right", fontsize=9)
            ax1.set_title("Monthly Income vs Expenses", color=c["text"], fontsize=13, pad=10)
            ax1.tick_params(colors=c["muted"])
            ax1.grid(True, alpha=0.15, color=c["border"])
            for spine in ax1.spines.values():
                spine.set_edgecolor(c["border"])
            legend = ax1.legend()
            for t in legend.get_texts():
                t.set_color(c["text"])
            legend.get_frame().set_facecolor(c["surface"])
            legend.get_frame().set_edgecolor(c["border"])
        else:
            ax1.text(0.5, 0.5, "No data available", ha="center", va="center",
                     color=c["muted"], fontsize=13)

        self.line_fig.tight_layout()
        self.line_canvas.draw()

        # ── NET CHART ──
        self.net_fig.clear()
        ax2 = self.net_fig.add_subplot(111)
        ax2.set_facecolor(c["surface"])
        self.net_fig.patch.set_facecolor(c["surface"])

        if months:
            xs = range(len(months))
            ax2.plot(xs, net, marker="o", linewidth=2.5, color=c["primary"])
            ax2.axhline(0, color=c["danger"], linestyle="--", alpha=0.4, linewidth=1.5)
            ax2.set_xticks(list(xs))
            ax2.set_xticklabels(month_labels, rotation=20, ha="right", fontsize=9)
            ax2.set_title("Net Savings Trend", color=c["text"], fontsize=13, pad=10)
            ax2.tick_params(colors=c["muted"])
            ax2.grid(True, alpha=0.15, color=c["border"])
            for spine in ax2.spines.values():
                spine.set_edgecolor(c["border"])
        else:
            ax2.text(0.5, 0.5, "No data available", ha="center", va="center",
                     color=c["muted"], fontsize=13)

        self.net_fig.tight_layout()
        self.net_canvas.draw()

    def _colors(self):
        theme = database.get_setting("theme", ThemeManager.DARK)
        return theme_colors(theme)

    def refresh_theme(self):
        self.load_data()
