from PySide6.QtCore import Qt
from PySide6.QtGui import QBitmap, QColor, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QApplication, QTableWidget

from app_styles import theme_colors


class RoundedTableWidget(QTableWidget):
    """Table that keeps row separators away from the rounded bottom corners."""

    RADIUS = 12

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._clip_viewport_to_bottom_radius()

    def paintEvent(self, event):
        super().paintEvent(event)
        self._paint_row_separators()
        self._paint_bottom_border()

    def _clip_viewport_to_bottom_radius(self):
        rect = self.viewport().rect()
        if rect.isEmpty():
            return

        radius = min(self.RADIUS, rect.width() // 2, rect.height() // 2)
        w = rect.width()
        h = rect.height()

        mask = QBitmap(rect.size())
        mask.fill(Qt.color0)

        path = QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(w, 0)
        path.lineTo(w, h - radius)
        path.quadTo(w, h, w - radius, h)
        path.lineTo(radius, h)
        path.quadTo(0, h, 0, h - radius)
        path.closeSubpath()

        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.color1)
        painter.drawPath(path)
        painter.end()

        self.viewport().setMask(mask)

    def _paint_bottom_border(self):
        rect = self.viewport().rect()
        if rect.isEmpty():
            return

        app = QApplication.instance()
        theme = app.property("theme") if app else "dark"
        color = QColor(theme_colors(theme).get("border", "#2d3f55"))

        radius = min(self.RADIUS, rect.width() // 2, rect.height() // 2)
        w = rect.width() - 1
        h = rect.height() - 1

        path = QPainterPath()
        path.moveTo(0, h - radius)
        path.quadTo(0, h, radius, h)
        path.lineTo(w - radius, h)
        path.quadTo(w, h, w, h - radius)

        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(QPen(color, 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)
        painter.end()

    def _paint_row_separators(self):
        if self.rowCount() <= 1:
            return

        app = QApplication.instance()
        theme = app.property("theme") if app else "dark"
        color = QColor(theme_colors(theme).get("border", "#2d3f55"))

        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.Antialiasing, False)
        painter.setPen(QPen(color, 1))

        left = 0
        right = self.viewport().width() - 1
        for row in range(self.rowCount() - 1):
            y = self.rowViewportPosition(row) + self.rowHeight(row) - 1
            if 0 <= y <= self.viewport().height():
                painter.drawLine(left, y, right, y)


def fit_table_height_to_rows(table, min_rows=0, max_rows=14, empty_height=60):
    """
    Resize the table so it shows exactly its rows with no blank space,
    and the rounded border-radius looks correct on all four corners.
    """
    table.resizeRowsToContents()

    row_count    = table.rowCount()
    visible_rows = max(min_rows, min(row_count, max_rows))

    row_height = 0
    for i in range(visible_rows):
        if i < row_count:
            row_height += table.rowHeight(i)
        else:
            row_height += table.verticalHeader().defaultSectionSize()

    if row_count == 0:
        row_height = max(row_height, empty_height)

    header_h = table.horizontalHeader().height()
    # A little extra room keeps the styled border and rounded viewport from
    # clipping the last row or action buttons on high-DPI Windows displays.
    total_h  = header_h + row_height + 6

    table.setMinimumHeight(total_h)
    table.setMaximumHeight(total_h)
    table.setViewportMargins(0, 0, 0, 0)
    if hasattr(table, "_clip_viewport_to_bottom_radius"):
        table._clip_viewport_to_bottom_radius()

    if row_count > max_rows:
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    else:
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


def apply_table_style(table):
    """
    Call after populating a table to ensure last row has no bottom border
    so it doesn't fight the rounded bottom corners.
    """
    row_count = table.rowCount()
    if row_count == 0:
        return
    last_row = row_count - 1
    for col in range(table.columnCount()):
        item = table.item(last_row, col)
        if item:
            # Mark last row so CSS :last child works
            item.setData(Qt.UserRole, "last")
