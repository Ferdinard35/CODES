# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'checkbox.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QLineEdit, QSizePolicy,
    QVBoxLayout, QWidget)
import sys

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(640, 480)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        self.lineEdit.setFont(font)

        self.verticalLayout.addWidget(self.lineEdit)

        self.checkBox_4 = QCheckBox(Form)
        self.checkBox_4.setObjectName(u"checkBox_4")
        font1 = QFont()
        font1.setFamilies([u"Segoe UI Variable"])
        font1.setPointSize(10)
        font1.setBold(True)
        self.checkBox_4.setFont(font1)

        self.verticalLayout.addWidget(self.checkBox_4)

        self.checkBox_5 = QCheckBox(Form)
        self.checkBox_5.setObjectName(u"checkBox_5")
        self.checkBox_5.setFont(font1)

        self.verticalLayout.addWidget(self.checkBox_5)

        self.checkBox_3 = QCheckBox(Form)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setFont(font1)
        self.checkBox_3.setStyleSheet(u"QCheckbox{color:\"red\"}")

        self.verticalLayout.addWidget(self.checkBox_3)

        self.checkBox_6 = QCheckBox(Form)
        self.checkBox_6.setObjectName(u"checkBox_6")
        self.checkBox_6.setFont(font1)
        self.checkBox_6.setStyleSheet(u"QLabel{rgb(0, 0, 0)}")

        self.verticalLayout.addWidget(self.checkBox_6)

        self.checkBox_2 = QCheckBox(Form)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setFont(font1)

        self.verticalLayout.addWidget(self.checkBox_2)

        self.checkBox = QCheckBox(Form)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setFont(font1)

        self.verticalLayout.addWidget(self.checkBox)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lineEdit.setText(QCoreApplication.translate("Form", u"Select one programming language", None))
        self.checkBox_4.setText(QCoreApplication.translate("Form", u"JAVA", None))
        self.checkBox_5.setText(QCoreApplication.translate("Form", u"C++", None))
        self.checkBox_3.setText(QCoreApplication.translate("Form", u"PYTHON", None))
        self.checkBox_6.setText(QCoreApplication.translate("Form", u"SWIFT", None))
        self.checkBox_2.setText(QCoreApplication.translate("Form", u"C#", None))
        self.checkBox.setText(QCoreApplication.translate("Form", u"JAVASCRIPT", None))
    # retranslateUi
app = QApplication(sys.argv)
Form = QWidget()
ui = Ui_Form()
ui.setupUi(Form)
Form.show()
sys.exit(app.exec())
