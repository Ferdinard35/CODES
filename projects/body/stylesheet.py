def apply_styles(app):
    app.setStyleSheet("""

    /* =========================
       MAIN WINDOW
    ========================= */
    QMainWindow {
        background: qlineargradient(
            x1:0, y1:0,
            x2:1, y2:1,
            stop:0 #1e272e,
            stop:1 #0f141a
        );
    }

    /* =========================
       LABELS
    ========================= */
    QLabel {
        color: #ecf0f1;
        font-size: 14px;
        font-family: Segoe UI;
    }

    /* =========================
       INPUT FIELDS
    ========================= */
    QLineEdit {
        background-color: #1e272e;
        color: white;
        border: 1px solid #3498db;
        border-radius: 6px;
        padding: 6px;
    }

    QLineEdit:focus {
        border: 2px solid #00FF7F;
    }

    /* =========================
       BUTTONS
    ========================= */
    QPushButton {
        background-color: #3498db;
        color: white;
        border-radius: 10px;
        padding: 10px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #2980b9;
    }

    QPushButton:pressed {
        background-color: #1f6aa5;
    }

    /* =========================
       TABLE
    ========================= */
    QTableWidget {
        background-color: #1e272e;
        color: white;
        gridline-color: #2c3e50;
        border: 1px solid #2c3e50;
        border-radius: 10px;
        font-size: 13px;
    }

    QHeaderView::section {
        background-color: #2c3e50;
        color: white;
        padding: 6px;
        font-weight: bold;
        border: none;
    }

    QTableWidget::item:selected {
        background-color: #00FF7F;
        color: black;
    }

    /* =========================
       SIDEBAR (IMPORTANT FIX)
    ========================= */
    QListWidget {
        background-color: #0f141a;
        border: none;
        color: white;
        padding: 5px;
    }

    QListWidget::item {
        padding: 12px;
        margin: 4px;
        border-radius: 6px;
    }

    QListWidget::item:hover {
        background-color: #2c3e50;
    }

    QListWidget::item:selected {
        background-color: #3498db;
        color: white;
        font-weight: bold;
    }

    /* =========================
       FRAMES (CARDS)
    ========================= */
    QFrame {
        background-color: #1e272e;
        border-radius: 12px;
    }

    """)