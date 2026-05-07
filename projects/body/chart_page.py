import sys
from PySide6.QtWidgets import  QVBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import database

class ChartPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # Create the matplotlib figure
        # Facecolor matches the slate blue UI
        self.fig = Figure(figsize=(5, 4), dpi=100, facecolor='#2c3e50') 
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)
        
        self.update_chart()

    def showEvent(self, event):
        """Refreshes the chart every time the page is shown"""
        self.update_chart()
        super().showEvent(event)

    def update_chart(self):
        # FEATURE ADDED: Ensure database.get_all_entries() uses "ORDER BY id ASC" 
        # so the lines connect chronologically based on when you added them.
        data = database.get_all_entries()
        goals = database.get_goals() 
        
        if not data:
            return

        dates = [row[0] for row in data]
        weights = [row[1] for row in data]

        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        # --- DARK THEME STYLING ---
        ax.set_facecolor('#1e272e') 
        
        # 1. Goal Zone Styling
        if goals and goals[0]:
            target_weight = goals[0]
            # Sunset Orange/Red Goal Zone
            ax.axhspan(target_weight - 2, target_weight + 2, color='#e74c3c', alpha=0.15, label="Target Range")
            ax.axhline(y=target_weight, color='#e74c3c', linestyle='--', linewidth=2, label="Goal")

        # 2. FEATURE ADDED: The "Juicy" Line
        # ax.plot (instead of scatter) ensures dots are connected by a solid line.
        ax.plot(dates, weights, marker='o', linestyle='-', color='#00FF7F', 
                linewidth=3, markersize=8, label="Weight Progress",
                markerfacecolor='#1e272e', markeredgewidth=2)
        
        # 3. Label & Tick Styling
        ax.set_title("Weight Progress Over Time", fontweight='bold', color='white', fontsize=14, pad=15)
        ax.set_ylabel("Weight (kg)", color='white', fontweight='bold')
        ax.set_xlabel("Entry Date", color='white', fontweight='bold')
        
        ax.tick_params(colors='white', labelsize=9)
        
        # Subtle Grid
        ax.grid(True, linestyle=':', alpha=0.2, color='white')
        
        # Clean Borders (Spines)
        for spine in ax.spines.values():
            spine.set_color('#3498db')
            spine.set_linewidth(1.5)

        # 4. Y-Axis Comfort Zone
        if goals and goals[0]:
            current_max = max(weights) if weights else target_weight
            current_min = min(weights) if weights else target_weight
            ax.set_ylim(current_min - 5, max(current_max, target_weight) + 5)

        # Clean up date overlapping
        self.fig.autofmt_xdate()
        self.fig.tight_layout() # Ensures labels don't get cut off
        self.canvas.draw()