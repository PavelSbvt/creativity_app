import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from gui.loading_start_window import MyLoadingWindow
from gui.main_window import mainWindow
from utils.output_rich import simple_log


def main() -> None:
    """
    Функция, запускающая загрузочное окно, которое по прошествии 3 секунд закроется,
     после чего откроется основное окно программы. Функция-связка.
    """

    app = QApplication(sys.argv)
    icon_path = Path('resources/images/icons/icon_pdf_maker_255_size.ico')
    app.setWindowIcon(QIcon(f"{icon_path.as_posix()}"))
    loading_win = MyLoadingWindow()
    loading_win.show()

    main_win = mainWindow()

    def on_loading_closed() -> None:
        """
        Функция, которая показывает основное окно,
         а загрузочное окно скрывает при показе основного окна программы.
        """
        simple_log("[I] Показ главного окна")
        main_win.show()
        loading_win.hide()
        simple_log("[I] загрузочное окно скрыто")

    loading_win.closed.connect(on_loading_closed)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()