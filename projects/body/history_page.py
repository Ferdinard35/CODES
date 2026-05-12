from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHeaderView,
    QAbstractItemView,
    QMessageBox,
    QLabel
)

from PySide6.QtCore import Qt
import database


class HistoryPage(QWidget):

    def __init__(self):
        super().__init__()

        # MAIN LAYOUT

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # GLOBAL MESSAGEBOX STYLE

        self.setStyleSheet("""
            QMessageBox {
                background-color: #111827;
            }

            QMessageBox QLabel {
                color: white;
                font-size: 14px;
            }

            QMessageBox QPushButton {
                background-color: #2563eb;
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
                min-width: 80px;
            }

            QMessageBox QPushButton:hover {
                background-color: #3b82f6;
            }
        """)

        # EMPTY STATE

        self.empty_label = QLabel("📭 No history available")
        self.empty_label.setAlignment(Qt.AlignCenter)

        self.empty_label.setStyleSheet("""
            color: #9ca3af;
            font-size: 18px;
            font-weight: bold;
            padding: 30px;
        """)

        self.layout.addWidget(self.empty_label)

        # TABLE

        self.table = QTableWidget()
        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Date",
            "Weight (kg)",
            "Waist (cm)",
            "Chest (cm)",
            "Arms (cm)",
            "BMI"
        ])

        # hide ID column
        self.table.setColumnHidden(0, True)

        # table behavior
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)

        self.table.verticalHeader().setDefaultSectionSize(55)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # TABLE STYLE

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #111827;
                alternate-background-color: #1f2937;
                color: #f9fafb;
                border: 1px solid #374151;
                border-radius: 16px;
                padding: 10px;
                font-size: 14px;
                gridline-color: transparent;
                selection-background-color: #2563eb;
                selection-color: white;
            }

            QHeaderView::section {
                background-color: #1e293b;
                color: #f3f4f6;
                border: none;
                border-bottom: 1px solid #374151;
                padding: 14px;
                font-weight: bold;
            }

            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #374151;
            }

            QTableWidget::item:hover {
                background-color: #1f2937;
            }
        """)

        self.layout.addWidget(self.table)

        # DELETE BUTTON

        self.del_btn = QPushButton("🗑 Delete Selected Entry")
        self.del_btn.setCursor(Qt.PointingHandCursor)

        self.del_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                border-radius: 12px;
                padding: 14px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }

            QPushButton:hover {
                background-color: #ef4444;
            }

            QPushButton:pressed {
                background-color: #b91c1c;
            }
        """)

        self.del_btn.clicked.connect(self.delete_entry)

        self.layout.addWidget(self.del_btn)

        # INITIAL LOAD

        self.load_data()

    # AUTO REFRESH

    def showEvent(self, event):
        self.load_data()
        super().showEvent(event)

    # LOAD DATA

    def load_data(self):

        self.table.setRowCount(0)

        try:
            data = database.get_all_history()

            print("DATA FROM DB:", data)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Database Error",
                str(e)
            )
            return

        if not data:
            self.table.hide()
            self.empty_label.show()
            return

        self.empty_label.hide()
        self.table.show()

        self.table.setRowCount(len(data))

        for row_idx, entry in enumerate(data):

            for col_idx, value in enumerate(entry):

                # handle empty values
                if value is None or value == "":
                    value = "--"

                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)

                self.table.setItem(row_idx, col_idx, item)

        self.table.resizeRowsToContents()

    # DELETE ENTRY

    def delete_entry(self):

        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Error",
                "Please select a row first"
            )
            return

        item = self.table.item(row, 0)

        if not item:
            return

        try:
            entry_id = int(item.text())

        except:
            QMessageBox.warning(
                self,
                "Error",
                "Invalid entry selected"
            )
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this entry?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            database.delete_entry(entry_id)
            self.load_data()