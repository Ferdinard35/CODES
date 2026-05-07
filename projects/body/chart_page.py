import sys
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import database

class ChartPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create the matplotlib figure
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)
        
        self.update_chart()

    def update_chart(self):
        data = database.get_all_entries()
        if not data:
            return

        dates = [row[0] for row in data]
        weights = [row[1] for row in data]

        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        # Plotting the data
        ax.plot(dates, weights, marker='o', linestyle='-', color='#2E86C1', linewidth=2)
        
        # Styling
        ax.set_title("Weight Progress Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Weight (kg)")
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Rotate dates for better visibility
        self.fig.autofmt_xdate()
        
        self.canvas.draw()