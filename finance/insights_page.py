"""
insights_page.py
================
UI page that displays AI-style smart spending insights.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt
from smart_insights import generate_insights
from refresh import refresh_manager


# Icon + colour per insight type
_STYLE = {
    "warning": ("⚠", "#f59e0b", "rgba(245,158,11,0.12)"),
    "danger":  ("✖", "#ef4444", "rgba(239,68,68,0.12)"),
    "success": ("✔", "#22c55e", "rgba(34,197,94,0.12)"),
    "info":    ("ℹ", "#3b82f6", "rgba(59,130,246,0.12)"),
    "tip":     ("💡", "#a78bfa", "rgba(167,139,250,0.12)"),
}


class InsightsPage(QWidget):

    def __init__(self):
        super().__init__()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.container = QWidget()
        self.main = QVBoxLayout(self.container)
        self.main.setContentsMargins(36, 36, 36, 36)
        self.main.setSpacing(0)

        self.scroll.setWidget(self.container)
        outer.addWidget(self.scroll)

        # Header
        title = QLabel("Smart Insights")
        title.setObjectName("PageTitle")
        self.main.addWidget(title)
        self.main.addSpacing(4)

        subtitle = QLabel(
            "AI-powered analysis of your spending patterns, budget usage, and saving habits."
        )
        subtitle.setObjectName("Subtitle")
        self.main.addWidget(subtitle)
        self.main.addSpacing(16)

        # Refresh button
        btn_row = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh Insights")
        self.refresh_btn.setObjectName("SecondaryButton")
        self.refresh_btn.setMinimumHeight(38)
        self.refresh_btn.setFixedWidth(180)
        self.refresh_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_btn.clicked.connect(self.load_insights)
        btn_row.addWidget(self.refresh_btn)
        btn_row.addStretch()
        self.main.addLayout(btn_row)
        self.main.addSpacing(16)

        # Placeholder for insight cards
        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setSpacing(12)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)

        self.main.addWidget(self.cards_container)
        self.main.addStretch()

        self.load_insights()
        refresh_manager.data_changed.connect(self.load_insights)

    def load_insights(self):
        # Clear old cards
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        insights = generate_insights()

        for ins in insights:
            self.cards_layout.addWidget(self._make_card(ins))

    def _make_card(self, ins: dict) -> QFrame:
        itype   = ins.get("type", "info")
        icon, color, bg = _STYLE.get(itype, _STYLE["info"])

        card = QFrame()
        card.setObjectName("InsightCard")
        card.setStyleSheet(f"""
            QFrame#InsightCard {{
                background-color: {bg};
                border: 1px solid {color}44;
                border-left: 4px solid {color};
                border-radius: 10px;
            }}
        """)

        row = QHBoxLayout(card)
        row.setContentsMargins(18, 16, 18, 16)
        row.setSpacing(14)

        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet(
            f"font-size:22px; color:{color}; background:transparent;"
        )
        icon_lbl.setFixedWidth(28)
        icon_lbl.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        text_col = QVBoxLayout()
        text_col.setSpacing(4)

        title_lbl = QLabel(ins.get("title", ""))
        title_lbl.setStyleSheet(
            f"font-size:14px; font-weight:700; color:{color}; background:transparent;"
        )

        msg_lbl = QLabel(ins.get("message", ""))
        msg_lbl.setObjectName("Subtitle")
        msg_lbl.setWordWrap(True)

        text_col.addWidget(title_lbl)
        text_col.addWidget(msg_lbl)

        row.addWidget(icon_lbl)
        row.addLayout(text_col)

        return card
