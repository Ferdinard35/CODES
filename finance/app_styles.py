COLORS = {
    "dark": {
        "background": "#0f172a",
        "surface": "#1e293b",
        "surface_alt": "#243347",
        "field": "#162032",
        "border": "#2d3f55",
        "text": "#f1f5f9",
        "muted": "#94a3b8",
        "header": "#1a2e44",
        "hover": "#263549",
        "primary": "#3b82f6",
        "primary_hover": "#2563eb",
        "success": "#22c55e",
        "danger": "#ef4444",
        "warning": "#f59e0b",
        "table_alt": "#172133",
        "sidebar": "#0f172a",
        "sidebar_hover": "#1e293b",
        "sidebar_active": "#3b82f6",
        "input_focus": "#3b82f6",
    },
    "light": {
        "background": "#f1f5f9",
        "surface": "#ffffff",
        "surface_alt": "#f8fafc",
        "field": "#ffffff",
        "border": "#e2e8f0",
        "text": "#0f172a",
        "muted": "#64748b",
        "header": "#f1f5f9",
        "hover": "#eff6ff",
        "primary": "#2563eb",
        "primary_hover": "#1d4ed8",
        "success": "#16a34a",
        "danger": "#dc2626",
        "warning": "#d97706",
        "table_alt": "#f8fafc",
        "sidebar": "#1e293b",
        "sidebar_hover": "#334155",
        "sidebar_active": "#2563eb",
        "input_focus": "#2563eb",
    },
}


def theme_colors(theme):
    return COLORS.get(theme, COLORS["dark"])


def get_stylesheet(theme):
    c = theme_colors(theme)

    return f"""
    /* ── BASE ── */
    QWidget {{
        background-color: {c["background"]};
        color: {c["text"]};
        font-family: "Segoe UI", system-ui, sans-serif;
        font-size: 14px;
    }}
    QMainWindow {{ background-color: {c["background"]}; }}

    /* ── SCROLL AREA ── */
    QScrollArea {{ background: transparent; border: none; }}
    QScrollArea > QWidget > QWidget {{ background: transparent; }}

    /* ── LABELS ── */
    QLabel {{
        background: transparent;
        color: {c["text"]};
    }}
    QLabel#PageTitle {{
        font-size: 22px;
        font-weight: 700;
        color: {c["text"]};
    }}
    QLabel#Subtitle {{
        color: {c["muted"]};
        font-size: 13px;
    }}
    QLabel#SectionTitle {{
        color: {c["text"]};
        font-size: 15px;
        font-weight: 700;
    }}
    QLabel#FieldLabel {{
        color: {c["muted"]};
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.06em;
    }}
    QLabel#MetricTitle {{
        font-size: 11px;
        font-weight: 600;
        color: {c["muted"]};
        letter-spacing: 0.06em;
    }}
    QLabel#MetricValue {{
        font-size: 24px;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: {c["text"]};
    }}
    QLabel#MetricValue[accent="primary"] {{ color: {c["primary"]}; }}
    QLabel#MetricValue[accent="success"] {{ color: {c["success"]}; }}
    QLabel#MetricValue[accent="danger"]  {{ color: {c["danger"]}; }}

    QLabel#StatusLabel[state="warning"] {{ color: {c["warning"]}; font-weight: 600; font-size: 13px; }}
    QLabel#StatusLabel[state="danger"]  {{ color: {c["danger"]};  font-weight: 600; font-size: 13px; }}
    QLabel#StatusLabel[state="success"] {{ color: {c["success"]}; font-weight: 600; font-size: 13px; }}

    /* ── CARDS ── */
    QFrame#Card,
    QFrame#FormCard,
    QFrame#TableCard,
    QFrame#ChartCard,
    QFrame#SettingsCard,
    QFrame#LoginCard {{
        background-color: {c["surface"]};
        border: 1px solid {c["border"]};
        border-radius: 12px;
    }}

    /* ── SIDEBAR ── */
    QFrame#Sidebar {{
        background-color: {c["sidebar"]};
        border-right: 1px solid {c["border"]};
    }}
    QLabel#SidebarBrand {{
        color: #f1f5f9;
        font-size: 16px;
        font-weight: 700;
        background: transparent;
    }}
    QFrame#SidebarDivider {{
        background-color: {c["border"]};
        border: none;
        max-height: 1px;
        min-height: 1px;
    }}

    /* ── SIDEBAR BUTTONS ── */
    QPushButton#SidebarButton {{
        background-color: transparent;
        color: {c["muted"]};
        border: none;
        border-radius: 8px;
        padding: 10px 14px;
        text-align: left;
        font-size: 13px;
        font-weight: 500;
    }}
    QPushButton#SidebarButton:hover {{
        background-color: {c["sidebar_hover"]};
        color: {c["text"]};
    }}
    QPushButton#SidebarButton[active="true"] {{
        background-color: {c["sidebar_active"]};
        color: #ffffff;
        font-weight: 600;
    }}

    /* ── SETTING ROW ── */
    QFrame#SettingRow {{
        background-color: transparent;
        border: none;
        border-bottom: 1px solid {c["border"]};
        min-height: 72px;
    }}

    /* ── INPUTS ── */
    QLineEdit,
    QTextEdit,
    QComboBox,
    QDateEdit {{
        background-color: {c["field"]};
        color: {c["text"]};
        border: 1px solid {c["border"]};
        border-radius: 8px;
        padding: 9px 12px;
        font-size: 14px;
        selection-background-color: {c["primary"]};
        selection-color: #ffffff;
    }}
    QLineEdit:focus,
    QTextEdit:focus,
    QComboBox:focus,
    QDateEdit:focus {{
        border: 1.5px solid {c["input_focus"]};
    }}
    QLineEdit:hover,
    QComboBox:hover,
    QDateEdit:hover {{
        border: 1px solid {c["primary"]};
    }}
    QComboBox::drop-down,
    QDateEdit::drop-down {{
        border: none;
        width: 32px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {c["surface"]};
        color: {c["text"]};
        border: 1px solid {c["border"]};
        selection-background-color: {c["primary"]};
        selection-color: #ffffff;
        padding: 4px;
    }}

    /* ── BUTTONS ── */
    QPushButton {{
        background-color: {c["primary"]};
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 10px 18px;
        font-size: 14px;
        font-weight: 600;
    }}
    QPushButton:hover {{ background-color: {c["primary_hover"]}; }}
    QPushButton:pressed {{ background-color: {c["primary_hover"]}; }}

    QPushButton#SuccessButton {{ background-color: {c["success"]}; color: #ffffff; }}
    QPushButton#SuccessButton:hover {{ background-color: #15803d; }}

    QPushButton#DangerButton {{ background-color: {c["danger"]}; color: #ffffff; }}
    QPushButton#DangerButton:hover {{ background-color: #b91c1c; }}

    QPushButton#SecondaryButton {{
        background-color: transparent;
        color: {c["primary"]};
        border: 1.5px solid {c["primary"]};
    }}
    QPushButton#SecondaryButton:hover {{ background-color: {c["hover"]}; }}

    QPushButton#LinkButton {{
        background-color: transparent;
        color: {c["primary"]};
        border: none;
        padding: 4px 8px;
        font-weight: 600;
        font-size: 13px;
    }}

    /* ── TOGGLE BUTTONS ── */
    QPushButton#ToggleInactive {{
        background-color: transparent;
        color: {c["muted"]};
        border: none;
        border-radius: 6px;
        padding: 6px 14px;
        font-size: 13px;
        font-weight: 500;
    }}
    QPushButton#ToggleInactive:hover {{
        background-color: {c["hover"]};
        color: {c["text"]};
    }}
    QPushButton#ToggleIncomeActive {{
        background-color: #16a34a;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 6px 14px;
        font-size: 13px;
        font-weight: 600;
    }}
    QPushButton#ToggleExpenseActive {{
        background-color: {c["danger"]};
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 6px 14px;
        font-size: 13px;
        font-weight: 600;
    }}

    /* ── TABLE ── */
    QTableWidget {{
        background-color: {c["surface"]};
        alternate-background-color: {c["table_alt"]};
        color: {c["text"]};
        border: 1px solid {c["border"]};
        border-radius: 12px;
        gridline-color: transparent;
        selection-background-color: {c["primary"]};
        selection-color: #ffffff;
        font-size: 13px;
    }}
    QTableWidget::item {{
        padding: 10px 14px;
        border-bottom: 1px solid {c["border"]};
    }}
    QTableWidget::item:selected {{
        background-color: {c["primary"]};
        color: #ffffff;
    }}
    QHeaderView {{
        background-color: {c["header"]};
        border-radius: 12px;
    }}
    QHeaderView::section {{
        background-color: {c["header"]};
        color: {c["muted"]};
        border: none;
        border-bottom: 1px solid {c["border"]};
        padding: 10px 14px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.06em;
    }}
    QHeaderView::section:first {{
        border-top-left-radius: 12px;
    }}
    QHeaderView::section:last {{
        border-top-right-radius: 12px;
    }}

    /* ── PROGRESS BAR ── */
    QProgressBar {{
        background-color: {c["surface_alt"]};
        border: none;
        border-radius: 6px;
        height: 12px;
        text-align: center;
        font-size: 12px;
        font-weight: 600;
    }}
    QProgressBar::chunk {{
        background-color: {c["primary"]};
        border-radius: 6px;
    }}

    /* ── SCROLLBAR ── */
    QScrollBar:vertical {{
        background: transparent;
        width: 6px;
        border-radius: 3px;
    }}
    QScrollBar::handle:vertical {{
        background: {c["border"]};
        border-radius: 3px;
        min-height: 30px;
    }}
    QScrollBar::handle:vertical:hover {{ background: {c["muted"]}; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
    QScrollBar:horizontal {{
        background: transparent;
        height: 6px;
        border-radius: 3px;
    }}
    QScrollBar::handle:horizontal {{
        background: {c["border"]};
        border-radius: 3px;
        min-width: 30px;
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0px; }}

    /* ── TOOLTIP / DIALOG / CALENDAR ── */
    QToolTip {{
        background-color: {c["surface"]};
        color: {c["text"]};
        border: 1px solid {c["border"]};
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 12px;
    }}
    QMessageBox {{ background-color: {c["surface"]}; }}
    QMessageBox QLabel {{ color: {c["text"]}; font-size: 14px; }}
    QDialog {{ background-color: {c["background"]}; }}
    QCalendarWidget QWidget {{ background-color: {c["surface"]}; color: {c["text"]}; }}
    QCalendarWidget QAbstractItemView {{
        background-color: {c["surface"]};
        color: {c["text"]};
        selection-background-color: {c["primary"]};
        selection-color: #ffffff;
    }}
    """
