def apply_styles(app):

    app.setStyleSheet("""

    QMainWindow {
        background-color: #0a0f1c;
    }

    QWidget {
        font-family: Segoe UI;
    }

    QLabel {
        color: #e2e8f0;
    }

    /* INPUTS */
    QLineEdit, QDateEdit {
        background-color: #111827;
        color: white;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 10px;
    }

    QLineEdit:focus, QDateEdit:focus {
        border: 1px solid #3b82f6;
    }

    /* BUTTONS */
    QPushButton {
        background-color: #2563eb;
        color: white;
        border-radius: 12px;
        padding: 10px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #3b82f6;
    }

    QPushButton:pressed {
        background-color: #1d4ed8;
    }

    /* CARDS */
    QFrame {
        background-color: #0f172a;
        border-radius: 18px;
        border: 1px solid #1f2937;
    }

    /* TABLE */
    QTableWidget {
        background-color: #0f172a;
        color: white;
        border-radius: 12px;
        gridline-color: #1f2937;
    }

    QHeaderView::section {
        background-color: #111827;
        color: #cbd5e1;
        border: none;
    }

    QTableWidget::item:selected {
        background-color: #3b82f6;
    }

    """)