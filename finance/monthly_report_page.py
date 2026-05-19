from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame
)

from PySide6.QtGui import QFont
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import database
from app_styles import theme_colors
from theme_manager import ThemeManager


class MonthlyReportPage(QWidget):

    def __init__(self):
        super().__init__()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(36, 36, 36, 36)
        outer.setSpacing(6)

        title = QLabel("Monthly Financial Reports")
        title.setObjectName("PageTitle")
        outer.addWidget(title)

        subtitle = QLabel("Compare income, expenses, and savings across months.")
        subtitle.setObjectName("Subtitle")
        outer.addWidget(subtitle)

        outer.addSpacing(16)

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

        outer.addSpacing(8)

        # ── CHARTS ──
        charts_row = QHBoxLayout()
        charts_row.setSpacing(16)

        c = self._colors()

        # Income vs Expense
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

        # Net savings
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

        self.load_data()

    def _metric_card(self, title, accent):
        card = QFrame()
        card.setObjectName("Card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 22, 24, 22)
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
            month = row[0]
            inc   = (row[1] or 0) / 100
            exp   = (row[2] or 0) / 100
            months.append(month)
            income.append(inc)
            expenses.append(exp)
            net.append(inc - exp)

        if net:
            best_i  = net.index(max(net))
            worst_i = net.index(min(net))
            avg     = sum(net) / len(net)

            self.best_val.setText(f"{months[best_i]}  +GHS {net[best_i]:,.2f}")
            self.worst_val.setText(f"{months[worst_i]}  GHS {net[worst_i]:,.2f}")
            self.avg_val.setText(f"GHS {avg:,.2f}")
        else:
            self.best_val.setText("—")
            self.worst_val.setText("—")
            self.avg_val.setText("—")

        # Refresh accent colors
        for v in [self.best_val, self.worst_val, self.avg_val]:
            v.style().unpolish(v)
            v.style().polish(v)

        # ── LINE CHART ──
        self.line_fig.clear()
        ax1 = self.line_fig.add_subplot(111)
        ax1.set_facecolor(c["surface"])
        self.line_fig.patch.set_facecolor(c["surface"])

        if months:
            ax1.plot(months, income,   marker="o", linewidth=2.5,
                     color=c["success"], label="Income")
            ax1.plot(months, expenses, marker="o", linewidth=2.5,
                     color=c["danger"],  label="Expenses")
            ax1.set_title("Monthly Income vs Expenses", color=c["text"], fontsize=13, pad=10)
            ax1.tick_params(colors=c["muted"])
            ax1.grid(True, alpha=0.15, color=c["border"])
            for spine in ax1.spines.values():
                spine.set_edgecolor(c["border"])
            legend = ax1.legend()
            for text in legend.get_texts():
                text.set_color(c["text"])
            legend.get_frame().set_facecolor(c["surface"])
            legend.get_frame().set_edgecolor(c["border"])
        else:
            ax1.text(0.5, 0.5, "No data available", ha="center", va="center",
                     color=c["muted"], fontsize=13)

        self.line_canvas.draw()

        # ── NET CHART ──
        self.net_fig.clear()
        ax2 = self.net_fig.add_subplot(111)
        ax2.set_facecolor(c["surface"])
        self.net_fig.patch.set_facecolor(c["surface"])

        if months:
            ax2.plot(months, net, marker="o", linewidth=2.5, color=c["primary"])
            ax2.axhline(0, color=c["danger"], linestyle="--", alpha=0.4, linewidth=1.5)
            ax2.set_title("Net Savings Trend", color=c["text"], fontsize=13, pad=10)
            ax2.tick_params(colors=c["muted"])
            ax2.grid(True, alpha=0.15, color=c["border"])
            for spine in ax2.spines.values():
                spine.set_edgecolor(c["border"])
        else:
            ax2.text(0.5, 0.5, "No data available", ha="center", va="center",
                     color=c["muted"], fontsize=13)

        self.net_canvas.draw()

    def _colors(self):
        theme = database.get_setting("theme", ThemeManager.DARK)
        return theme_colors(theme)

    def refresh_theme(self):
        self.load_data()
