from PySide6.QtCore import QObject, Signal


class RefreshManager(QObject):

    # Signal emitted whenever transaction data changes
    data_changed = Signal()


# Global shared refresh manager
refresh_manager = RefreshManager()