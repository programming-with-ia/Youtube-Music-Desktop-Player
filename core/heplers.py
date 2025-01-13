from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import QRect


class Helper:
    @classmethod
    def get_centered_geometry(cls, width, height):
        screen_geometry = QDesktopWidget().screenGeometry()
        x = (screen_geometry.width() - width) // 2
        y = (screen_geometry.height() - height) // 2
        return QRect(x, y, width, height)

    def do_nothing(v):
        return v
