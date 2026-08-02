

def center_window(self) -> None:
    """
    функция для центрирования главного окна, чтобы оно появлялось
    по центру экрана пользователя после исчезновения загрузочного окна
    """

    qr = self.frameGeometry()
    cp = self.screen().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())
