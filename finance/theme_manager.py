from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication

import database


class ThemeManager:

    DARK = "dark"
    LIGHT = "light"

    @staticmethod
    def apply_theme(app: QApplication, theme="dark"):

        if theme == ThemeManager.DARK:
            ThemeManager.apply_dark(app)
        else:
            ThemeManager.apply_light(app)

        database.set_setting("theme", theme)

    @staticmethod
    def apply_dark(app):

        palette = QPalette()

        palette.setColor(QPalette.Window, QColor("#0f172a"))
        palette.setColor(QPalette.WindowText, QColor("#ffffff"))
        palette.setColor(QPalette.Base, QColor("#1e293b"))
        palette.setColor(QPalette.AlternateBase, QColor("#334155"))
        palette.setColor(QPalette.Text, QColor("#ffffff"))
        palette.setColor(QPalette.Button, QColor("#1e293b"))
        palette.setColor(QPalette.ButtonText, QColor("#ffffff"))

        app.setPalette(palette)

    @staticmethod
    def apply_light(app):

        palette = QPalette()

        palette.setColor(QPalette.Window, QColor("#f1f5f9"))
        palette.setColor(QPalette.WindowText, QColor("#0f172a"))
        palette.setColor(QPalette.Base, QColor("#ffffff"))
        palette.setColor(QPalette.AlternateBase, QColor("#e2e8f0"))
        palette.setColor(QPalette.Text, QColor("#0f172a"))
        palette.setColor(QPalette.Button, QColor("#e2e8f0"))
        palette.setColor(QPalette.ButtonText, QColor("#0f172a"))

        app.setPalette(palette)