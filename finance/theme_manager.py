from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication

import database
from app_styles import get_stylesheet, theme_colors


class ThemeManager:

    DARK = "dark"
    LIGHT = "light"

    @staticmethod
    def apply_theme(app, theme="dark", save=True):
        theme = ThemeManager.normalize_theme(theme)
        target_app = QApplication.instance() or app
        colors = theme_colors(theme)

        palette = QPalette()
        palette.setColor(QPalette.Window,          QColor(colors["background"]))
        palette.setColor(QPalette.WindowText,      QColor(colors["text"]))
        palette.setColor(QPalette.Base,            QColor(colors["field"]))
        palette.setColor(QPalette.AlternateBase,   QColor(colors["surface_alt"]))
        palette.setColor(QPalette.Text,            QColor(colors["text"]))
        palette.setColor(QPalette.Button,          QColor(colors["primary"]))
        palette.setColor(QPalette.ButtonText,      QColor("#ffffff"))
        palette.setColor(QPalette.Highlight,       QColor(colors["primary"]))
        palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))

        target_app.setPalette(palette)
        target_app.setProperty("theme", theme)
        target_app.setStyleSheet(get_stylesheet(theme))

        if save:
            database.set_setting("theme", theme)

    @staticmethod
    def normalize_theme(theme):
        if theme not in [ThemeManager.DARK, ThemeManager.LIGHT]:
            return ThemeManager.DARK
        return theme
