def apply_styles(app):

    app.setStyleSheet("""

    /* ================= GLOBAL ================= */
    QMainWindow {
        background-color: #0a0f1c;
    }

    QWidget {
        font-family: "Segoe UI";
        font-size: 13px;
    }

    QLabel {
        color: #e2e8f0;
    }

    /* ================= INPUTS ================= */
    QLineEdit, QDateEdit, QComboBox {
        background-color: #111827;
        color: white;
        border: 1px solid #1f2937;
        border-radius: 12px;

        /* 🔥 FIXED PADDING (this was inconsistent before) */
        padding: 10px 12px;
        min-height: 38px;
    }

    QLineEdit:focus, QDateEdit:focus, QComboBox:focus {
        border: 1px solid #3b82f6;
        background-color: #0f1a2b;
    }

    /* ================= BUTTONS ================= */
    QPushButton {
        background-color: #2563eb;
        color: white;

        border-radius: 12px;

        /* 🔥 more balanced button spacing */
        padding: 10px 14px;

        font-weight: 600;
        min-height: 38px;
    }

    QPushButton:hover {
        background-color: #3b82f6;
    }

    QPushButton:pressed {
        background-color: #1d4ed8;
        padding-top: 11px;   /* subtle press effect */
        padding-left: 13px;
    }

    /* ================= CARDS ================= */
    QFrame {
        background-color: #0f172a;
        border-radius: 20px;
        border: 1px solid #1f2937;

        /* 🔥 FIXED: breathing space inside cards */
        padding: 6px;
    }

    /* ================= TABLES ================= */
    QTableWidget {
        background-color: #0f172a;
        color: white;
        border-radius: 12px;
        gridline-color: #1f2937;

        selection-background-color: #1d4ed8;
        outline: none;
    }

    QHeaderView::section {
        background-color: #111827;
        color: #cbd5e1;
        border: none;
        padding: 8px;
        font-weight: 600;
    }

    QTableWidget::item {
        padding: 8px;
    }

    QTableWidget::item:selected {
        background-color: #3b82f6;
    }

    /* ================= SCROLLBARS (BIG UPGRADE) ================= */
    QScrollBar:vertical {
        background: #0f172a;
        width: 10px;
        border-radius: 5px;
    }

    QScrollBar::handle:vertical {
        background: #1f2937;
        border-radius: 5px;
    }

    QScrollBar::handle:vertical:hover {
        background: #3b82f6;
    }

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        height: 0;
    }

    """)