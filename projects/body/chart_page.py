from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from datetime import datetime
import database


class ChartPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        # Figure styling
        self.fig = Figure(figsize=(5, 4), dpi=100, facecolor="#1e1e2f")
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#12121a")

        # initial draw
        self.update_chart()

    def showEvent(self, event):
        """Auto refresh when page is opened"""
        self.update_chart()
        super().showEvent(event)

    def update_chart(self):
        data = database.get_all_entries()

        self.ax.clear()
        self.ax.set_facecolor("#12121a")

        if not data:
            self.ax.text(
                0.5, 0.5,
                "No data available",
                transform=self.ax.transAxes,
                ha="center",
                va="center",
                color="white",
                fontsize=14
            )
            self.canvas.draw()
            return

        # ✅ SORT DATA BY DATE (IMPORTANT FIX)
        data.sort(key=lambda x: x[0])

        dates = [
            datetime.strptime(row[0], "%Y-%m-%d")
            for row in data
        ]
        weights = [row[1] for row in data]

        # Line chart
        self.ax.plot(
            dates,
            weights,
            marker="o",
            linestyle="-",
            color="#00ff88",
            linewidth=2
        )

        # Styling
        self.ax.set_title("Weight Progress", color="white", fontsize=12)
        self.ax.tick_params(colors="white")

        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

        self.fig.autofmt_xdate()
        self.canvas.draw()