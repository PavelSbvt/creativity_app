from PyQt6.QtGui import QResizeEvent


def center_window(self):
    """
    Центрирует окно на экране пользователя
    """

    # Получаем геометрию окна
    frame_geometry = self.frameGeometry()

    # Получаем геометрию экрана
    screen_geometry = self.screen().availableGeometry()

    # Вычисляем центр экрана
    center_point = screen_geometry.center()

    # Перемещаем окно в центр
    frame_geometry.moveCenter(center_point)
    self.move(frame_geometry.topLeft())

def handleResizeEvent(window, event: QResizeEvent):
    """
    Обработчик изменения размера окна
    """

    new_size = event.size()
    # old_size = event.oldSize()

    print(f"Новый размер: {new_size.width()}x{new_size.height()}")
    # print(f"Старый размер: {old_size.width()}x{old_size.height()}")

    return new_size