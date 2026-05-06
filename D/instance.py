import sys
from PySide6.QtWidgets import(QApplication,QMainWindow,QInputDialog,QLineEdit,QPushButton,QVBoxLayout,QWidget)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        
        layout = QVBoxLayout()
        button1=QPushButton("Integer")
        button1.clicked.connect(self.get_an_integer)
        layout.addWidget(button1)
        
        button2=QPushButton("Float")
        button2.clicked.connect(self.get_a_float)
        layout.addWidget(button2)

        
        button3=QPushButton("Select")
        button3.clicked.connect(self.get_a_str_from_list)
        layout.addWidget(button3)

        button4=QPushButton("Select")
        button4.clicked.connect(self.get_a_str)
        layout.addWidget(button4)
        
        button5=QPushButton("Text")
        button5.clicked.connect(self.get_a_text)
        layout.addWidget(button5)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    def get_an_integer(self):
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Enter an Integer")
        dialog.setLabelText("Type your integer here")
        dialog.setIntValue(0)
        dialog.setIntMinimum(-5)
        dialog.setIntMaximum(5)
        dialog.setIntStep(1)

        ok = dialog.exec()
        print("Result:",ok, dialog.intValue())
    def get_a_float(self):
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Enter a Float")
        dialog.setLabelText("Type a float here")
        dialog.setDoubleValue(0.1)
        dialog.setDoubleMinimum(-5.3)
        dialog.setDoubleMaximum(5.7)
        dialog.setDoubleStep(1.4)
        dialog.setDoubleDecimals(2)

        ok = dialog.exec()
        print("Result:",ok, dialog.doubleValue())

    def get_a_str_from_list(self):
        dialog = QInputDialog(self)
        dialog.setWindowTitle("select a String ")
        dialog.setLabelText("Select a fruit from the list:")
        items = ["Apple", "pear", "orange", "grape"]
        dialog.setComboBoxItems(items)
        dialog.setComboBoxEditable(False)
        dialog.setTextValue(items[2])
        ok = dialog.exec()
        print("Result:",ok, dialog.textValue())

    def get_a_str(self):
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Enter a String")
        dialog.setLabelText("Type your password")
        dialog.setTextValue("my secret password")
        dialog.setTextEchoMode(QLineEdit.Password)

        ok = dialog.exec()
        print("Result:",ok, dialog.textValue())
    def get_a_text(self):
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Enter Text")
        dialog.setLabelText("Type your novel here")
        dialog.setTextValue("Once upon a time...")
        dialog.setOption(QInputDialog.UsePlainTextEditForTextInput,True)    

        ok = dialog.exec()
        print("Result:",ok, dialog.textValue())
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()