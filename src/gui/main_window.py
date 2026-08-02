from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.QtGui import QResizeEvent

from utils.functions_determining_state_user_window import handleResizeEvent, center_window


class mainWindow(QWidget):
    """
    Класс главного окна приложения
    """

    def __init__(self):
        super().__init__()

        self.resize(200, 200)

        # фоновый блок для главного окна
        self.bg_widget = QWidget(self)
        self.bg_widget.setStyleSheet("background-color: white; border-radius: 10px;")
        self.bg_widget.setFixedSize(100,100)
        self.bg_widget.move(0,0)

        center_window(self)

    def resizeEvent(self, event: QResizeEvent):
        """
        Вызывается каждый раз, когда окно изменяет размер
        """
        handleResizeEvent(self, event)




