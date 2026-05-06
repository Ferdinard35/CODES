from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout,QGroupBox,QLabel,QRadioButton,QHBoxLayout
from PySide6.QtGui import QIcon,QFont
import sys
 
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dance")
        self.setWindowIcon(QIcon("icon.png"))
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: green;")
        self.radio_btn()
        vbox = QVBoxLayout()
        vbox.addWidget(self.grpbox)
        self.setLayout(vbox)
        self.label = QLabel("No dance style selected")
        self.label.setFont(QFont("Arial", 12))
        vbox.addWidget(self.label)

    def radio_btn(self):
        self.grpbox = QGroupBox("Select Dance Style")
        self.grpbox.setFont(QFont("Arial", 12, QFont.Bold))
        hbox = QHBoxLayout()
        self.radio1 = QRadioButton("Ballet")
        self.radio1.setChecked(True)
        self.radio1.toggled.connect(self.on_selected)
        self.radio2 = QRadioButton("Hip Hop")
        self.radio2.toggled.connect(self.on_selected)
        self.radio3 = QRadioButton("Salsa")
        self.radio3.toggled.connect(self.on_selected)
        self.radio4 = QRadioButton("Tango")
        self.radio4.toggled.connect(self.on_selected)
        self.radio1.setFont(QFont("Arial", 10))
        self.radio2.setFont(QFont("Arial", 10))
        self.radio3.setFont(QFont("Arial", 10))
        self.radio4.setFont(QFont("Arial", 10))
        hbox.addWidget(self.radio1)
        hbox.addWidget(self.radio2)
        hbox.addWidget(self.radio3)
        hbox.addWidget(self.radio4)
        self.grpbox.setLayout(hbox)
    
    def on_selected(self):
        radio = self.sender()
        if radio.isChecked():
            self.label.setText(f"Selected dance style: {radio.text()}")




app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()        