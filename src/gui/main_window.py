from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.QtGui import QResizeEvent

from utils.functions_determining_state_user_window import handleResizeEvent, center_window


class mainWindow(QWidget):
    """
    Класс главного окна приложения
    """

    def __init__(self):
        super().__init__()

        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: white;")

        #
        self.cap_widget = QWidget(self)
        self.cap_widget.setStyleSheet("background-color: orange;")
        self.cap_widget.setFixedSize(self.width(),50)
        self.cap_widget.move(0,0)

        center_window(self)

    def resizeEvent(self, event: QResizeEvent):
        """
        Обработчик изменения размера окна
        """

        new_size = event.size()

        new_width = new_size.width()
        new_height = new_size.height()

        self.cap_widget.setFixedSize(new_width, 50)
