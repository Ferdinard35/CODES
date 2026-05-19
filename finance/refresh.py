from PySide6.QtCore import QObject, Signal


class RefreshManager(QObject):

    data_changed = Signal()

    def __init__(self):
        super().__init__()

    def trigger_refresh(self):
        self.data_changed.emit()

    def reset(self):
        try:
            self.data_changed.disconnect()
        except Exception:
            pass


refresh_manager = RefreshManager()
