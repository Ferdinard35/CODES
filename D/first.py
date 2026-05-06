from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton,QLabel,QVBoxLayout
from PySide6.QtGui import QFont,QIcon
import sys
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dance")
        self.setWindowIcon(QIcon("icon.png"))
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: green;")
        self.create_button()
        layout = QVBoxLayout()
        btn1 = QPushButton("Button 1")
        layout.addWidget(btn1)
        self.setLayout(layout)  


    def create_button(self):
        button = QPushButton("Click Me", self)
        button.setGeometry(150, 130, 100, 40)
        button.setStyleSheet("background-color: white; color: black; font-size: 16px;")
        button.setIcon(QIcon("icon.png")) 
        button.clicked.connect(self.clicked_button)
        
        self.label = QLabel("Welcome to the Dance App!", self)
       # self.label.move(100, 50)
        self.label.setStyleSheet("color: white;")
        self.label.setFont(QFont("Arial", 18, QFont.Bold))
        self.label.adjustSize()  
         
    def clicked_button(self):
        self.label.setText("Button Clicked!")
        self.label.setStyleSheet("color: red;")


app = QApplication(sys.argv)
window = MainWindow()
window.show()      
app.exec()