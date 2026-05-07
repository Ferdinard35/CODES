# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'radiobutton.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QWidget)
import sys

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(640, 480)
        self.radioButton = QRadioButton(Form)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(0, 130, 98, 24))
        self.radioButton_2 = QRadioButton(Form)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(10, 210, 98, 24))
        self.radioButton_3 = QRadioButton(Form)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setGeometry(QRect(10, 290, 98, 24))
        self.radioButton_4 = QRadioButton(Form)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setGeometry(QRect(10, 380, 98, 24))
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(550, 440, 81, 26))
        self.radioButton_5 = QRadioButton(Form)
        self.radioButton_5.setObjectName(u"radioButton_5")
        self.radioButton_5.setGeometry(QRect(240, 130, 98, 24))
        self.radioButton_6 = QRadioButton(Form)
        self.radioButton_6.setObjectName(u"radioButton_6")
        self.radioButton_6.setGeometry(QRect(250, 220, 98, 24))
        self.radioButton_7 = QRadioButton(Form)
        self.radioButton_7.setObjectName(u"radioButton_7")
        self.radioButton_7.setGeometry(QRect(250, 290, 98, 24))
        self.radioButton_8 = QRadioButton(Form)
        self.radioButton_8.setObjectName(u"radioButton_8")
        self.radioButton_8.setGeometry(QRect(250, 380, 98, 24))
        self.radioButton_9 = QRadioButton(Form)
        self.radioButton_9.setObjectName(u"radioButton_9")
        self.radioButton_9.setGeometry(QRect(460, 130, 98, 24))
        self.radioButton_10 = QRadioButton(Form)
        self.radioButton_10.setObjectName(u"radioButton_10")
        self.radioButton_10.setGeometry(QRect(460, 220, 98, 24))
        self.radioButton_11 = QRadioButton(Form)
        self.radioButton_11.setObjectName(u"radioButton_11")
        self.radioButton_11.setGeometry(QRect(470, 290, 98, 24))
        self.radioButton_12 = QRadioButton(Form)
        self.radioButton_12.setObjectName(u"radioButton_12")
        self.radioButton_12.setGeometry(QRect(470, 380, 98, 24))
        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(0, 40, 331, 31))
        font = QFont()
        font.setFamilies([u"Segoe UI Variable Small"])
        font.setPointSize(18)
        font.setBold(True)
        self.lineEdit.setFont(font)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.radioButton.setText(QCoreApplication.translate("Form", u"Mouse", None))
        self.radioButton_2.setText(QCoreApplication.translate("Form", u"Keyboard", None))
        self.radioButton_3.setText(QCoreApplication.translate("Form", u"Monitor", None))
        self.radioButton_4.setText(QCoreApplication.translate("Form", u"Trackpad", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"OK", None))
        self.radioButton_5.setText(QCoreApplication.translate("Form", u"System unit", None))
        self.radioButton_6.setText(QCoreApplication.translate("Form", u"Printer", None))
        self.radioButton_7.setText(QCoreApplication.translate("Form", u"Scanner", None))
        self.radioButton_8.setText(QCoreApplication.translate("Form", u"Fax machine", None))
        self.radioButton_9.setText(QCoreApplication.translate("Form", u"Plotter", None))
        self.radioButton_10.setText(QCoreApplication.translate("Form", u"Projector", None))
        self.radioButton_11.setText(QCoreApplication.translate("Form", u"Headset", None))
        self.radioButton_12.setText(QCoreApplication.translate("Form", u"Headphone", None))
        self.lineEdit.setText(QCoreApplication.translate("Form", u"Select one", None))
    # retranslateUi


app = QApplication(sys.argv)
Form = QWidget()
ui = Ui_Form()
ui.setupUi(Form)
Form.show()
sys.exit(app.exec())
