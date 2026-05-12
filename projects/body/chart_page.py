from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame
)

from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.dates as mdates
import mplcursors

from datetime import datetime
import database


class ChartPage(QWidget):

    def __init__(self):
        super().__init__()

        # MAIN LAYOUT
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(25)

        # TITLE
        self.title = QLabel("📈 Weight Analytics")
        self.title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.title.setStyleSheet("color: white;")
        self.layout.addWidget(self.title)

        # SUBTITLE
        self.subtitle = QLabel("Track your body weight progress over time.")
        self.subtitle.setStyleSheet("color: #94a3b8; font-size: 14px;")
        self.layout.addWidget(self.subtitle)

        # CARD CONTAINER
        self.card = QFrame()
        self.card.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border-radius: 22px;
                border: 1px solid #1f2937;
            }
        """)

        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setContentsMargins(25, 25, 25, 25)

        # MATPLOTLIB FIGURE
        self.fig = Figure(figsize=(5, 4), dpi=100, facecolor="#111827")
        self.canvas = FigureCanvas(self.fig)
        self.card_layout.addWidget(self.canvas)

        self.layout.addWidget(self.card)

        # AXIS
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#111827")

        # INITIAL DRAW
        self.update_chart()

    # REFRESH WHEN PAGE OPENS
    def showEvent(self, event):
        self.update_chart()
        super().showEvent(event)

    # UPDATE CHART
    def update_chart(self):

        data = database.get_all_entries()
        goals = database.get_goals()

        self.ax.clear()
        self.ax.set_facecolor("#111827")

        # NO DATA CASE
        if not data:
            self.ax.text(
                0.5, 0.5,
                "No chart data available",
                transform=self.ax.transAxes,
                ha="center",
                va="center",
                color="#94a3b8",
                fontsize=15
            )
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.canvas.draw()
            return

        # SORT DATA
        data.sort(key=lambda x: x[0])

        dates = [
            datetime.strptime(row[0], "%Y-%m-%d")
            for row in data
        ]
        weights = [row[1] for row in data]

        # PLOT LINE
        line, = self.ax.plot(
            dates,
            weights,
            color="#3b82f6",
            linewidth=3,
            marker="o",
            markersize=8,
            markerfacecolor="#60a5fa",
            markeredgewidth=2,
            markeredgecolor="#dbeafe"
        )

        # TOOLTIP HOVER
        cursor = mplcursors.cursor(line, hover=True)

        @cursor.connect("add")
        def on_add(sel):
            x, y = sel.target
            hover_date = mdates.num2date(x)

            sel.annotation.set_text(
                f"{y:.1f} kg\n{hover_date.strftime('%b %d, %Y')}"
            )

            sel.annotation.get_bbox_patch().set(
                fc="#0f172a",
                ec="#3b82f6",
                alpha=0.95
            )

            sel.annotation.arrow_patch.set_color("#3b82f6")

        # GOAL LINE + STATUS
        if goals and goals.get("target_weight"):

            goal_weight = goals["target_weight"]

            self.ax.axhline(
                y=goal_weight,
                color="#22c55e",
                linestyle="--",
                linewidth=2,
                alpha=0.9
            )

            self.ax.text(
                dates[0],
                goal_weight + 1,
                f"Goal: {goal_weight} kg",
                color="#22c55e",
                fontsize=10,
                fontweight="bold",
                backgroundcolor="#111827"
            )

            latest_weight = weights[-1]

            if latest_weight > goal_weight:
                status = f"+{latest_weight - goal_weight:.1f} kg"
                status_color = "#ef4444"

            elif latest_weight < goal_weight:
                status = f"-{goal_weight - latest_weight:.1f} kg"
                status_color = "#22c55e"

            else:
                status = "Goal reached"
                status_color = "#3b82f6"

            self.ax.text(
                0.98,
                0.97,
                status,
                transform=self.ax.transAxes,
                fontsize=9,
                color="white",
                horizontalalignment='right',
                verticalalignment='top',
                bbox=dict(
                    boxstyle="round,pad=0.3",
                    facecolor=status_color,
                    edgecolor="none",
                    alpha=0.9
                )
            )

        # GRID
        self.ax.grid(True, linestyle="--", alpha=0.15)

        # TITLE + LABELS
        self.ax.set_title(
            "Weight Progress",
            color="white",
            fontsize=18,
            pad=20,
            fontweight="bold"
        )

        self.ax.set_xlabel("Date", color="#cbd5e1", fontsize=11, labelpad=10)
        self.ax.set_ylabel("Weight (kg)", color="#cbd5e1", fontsize=11, labelpad=10)

        # TICKS
        self.ax.tick_params(axis="x", colors="#cbd5e1", labelsize=10)
        self.ax.tick_params(axis="y", colors="#cbd5e1", labelsize=10)

        # SPINES
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["left"].set_color("#334155")
        self.ax.spines["bottom"].set_color("#334155")

        # DATE FORMAT
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        self.fig.autofmt_xdate()

        # FINAL DRAW
        self.fig.tight_layout()
        self.canvas.draw()