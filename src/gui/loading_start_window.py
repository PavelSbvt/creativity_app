from datetime import datetime
from pathlib import Path
import random

from PyQt6.QtCore import QPoint, QTimer, pyqtSignal, Qt
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtWidgets import (QLabel, QWidget, QVBoxLayout, QProgressBar, QFrame)

from utils.output_rich import enter_log, debug_log, warning_log
from gui.animations.animations_for_windows import (animationAppearanceWindow,
animationDindisappearanceAndClosing)
from utils.functions_for_window_gui import center_window, getMainColorImage
from utils.citations import QUOTES


class MyLoadingWindow(QWidget):
    """
    Класс загрузочного окна на PyQt6 с гиф-анимацией загрузки
    """

    closed = pyqtSignal()

    def __init__(self) -> None:
        """
        Инициализация загрузочного окна с гиф-анимацией.
        """

        super().__init__()

        # Добавляю новые семейства шрифтов из ресурсов проекта.
        front_Inter_italic_path = Path("resources/fonts/Inter/Inter-Italic-VariableFont_opsz,wght.ttf")
        font_Inter_path = Path("resources/fonts/Inter/Inter-VariableFont_opsz,wght.ttf")

        font_Inter_italic_id = QFontDatabase.addApplicationFont(front_Inter_italic_path.as_posix())
        font_Inter_id = QFontDatabase.addApplicationFont(font_Inter_path.as_posix())

        self.font_family_Inter = QFontDatabase.applicationFontFamilies(font_Inter_id)[0]
        self.font_family_Inter_italic = QFontDatabase.applicationFontFamilies(font_Inter_italic_id)[0]

        font_Playfair_Display_path = Path("resources/fonts/Playfair_Display/PlayfairDisplay-VariableFont_wght.ttf")
        font_Playfair_Display_italic_path = Path("resources/fonts/Playfair_Display/PlayfairDisplay-Italic-VariableFont_wght.ttf")

        font_Playfair_Display_id = QFontDatabase.addApplicationFont(font_Playfair_Display_path.as_posix())
        font_Playfair_Display_italic_id = QFontDatabase.addApplicationFont(font_Playfair_Display_italic_path.as_posix())

        self.font_family_Playfair_Display = QFontDatabase.applicationFontFamilies(font_Playfair_Display_id)[0]
        self.font_family_Playfair_Display_italic = QFontDatabase.applicationFontFamilies(font_Playfair_Display_italic_id)[0]

        self.drag_position: QPoint = QPoint()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.close_window_animation = None

        enter_log("[Enter] показ загрузочного окна.")

        # Виджет для фона (большой тёмный)
        self.widget_background_fill = QWidget(self)
        self.widget_background_fill.setStyleSheet("background-color: rgb(43, 43, 43); border-radius: 10px;")
        self.widget_background_fill.setFixedSize(780, 520)
        self.widget_background_fill.move(0, 0)

        # виджет с градиентом от главного цвета изображения до цвета главного фона
        self.widget_gradient = QWidget(self)
        self.widget_gradient.setFixedSize(780, 520)
        self.widget_gradient.move(0,0)

        # фото
        self.loading_window = QWidget(self)
        self.loading_window.setFixedSize(390,500)
        self.loading_window.move(380,10)

        debug_log("[I] вывод сообщения о сообщения о загрузке ('Приложение загружается...')")

        # Сообщение о загрузке
        self.lb_blс_m_load = QLabel(self)
        self.lb_blс_m_load.setText("Приложение загружается, подождите, пожалуйста...")
        self.lb_blс_m_load.setStyleSheet("color: rgb(169, 183, 198);")
        self.lb_blс_m_load.setFont(QFont(self.font_family_Inter, 10))
        self.lb_blс_m_load.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lb_blс_m_load.setGeometry(0, 490, 370, 30)
        self.lb_blс_m_load.setWordWrap(True)

        # Название приложения
        self.block_app_name = QLabel(self)
        self.block_app_name.setStyleSheet("color: white; font: bold;")
        self.block_app_name.setFont(QFont(self.font_family_Playfair_Display, 30))
        self.block_app_name.setText("📷 Creativity")
        self.block_app_name.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.block_app_name.setGeometry(10,0,370,50)

        # фон текста
        self.background_widget_text = QWidget(self)
        self.background_widget_text.setStyleSheet("background-color: rgba(255, 255, 255, 0.03); border-radius: 10px;")
        self.background_widget_text.setFixedSize(360, 150)
        self.background_widget_text.move(10,60)
        self.label_text = QLabel(self.background_widget_text)
        self.label_text.setText("Creativity - приложение для фотографов и творческих людей. Здесь Вы сможете размещать свои фотографии и многое другое (в разработке).")
        self.label_text.setWordWrap(True)
        self.label_text.setFont(QFont(self.font_family_Inter, 12))
        self.label_text.setGeometry(10,50, 340, 130)
        self.label_text.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Текст приветствия (меняется по времени суток)
        self.lb_hi_prog = QLabel(self)
        self.lb_hi_prog.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lb_hi_prog.setFont(QFont(self.font_family_Playfair_Display, 20))
        self.lb_hi_prog.setGeometry(10, 60, 370, 40)

        # Виджет для цитат
        self.citation = QWidget(self)
        self.citation.setFixedSize(360, 240)
        self.citation.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
        """)
        self.citation.move(10, 225)

        # Лайаут
        self.citation_layout = QVBoxLayout()
        self.citation_layout.setSpacing(10)
        self.citation_layout.setContentsMargins(10, 10, 10, 10)

        citation_text, author_text = self.getCitationWithAuthor()

        # Цитата
        self.citation_label = QLabel()
        self.citation_label.setText(citation_text)
        self.citation_label.setWordWrap(True)
        self.citation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if len(citation_text) < 37:
            self.citation_label.setFont(QFont(self.font_family_Playfair_Display, 18))
        elif len(citation_text) < 70:
            self.citation_label.setFont(QFont(self.font_family_Playfair_Display, 14))
        elif len(citation_text) < 150:
            self.citation_label.setFont(QFont(self.font_family_Playfair_Display, 12))
        else:
            self.citation_label.setFont(QFont(self.font_family_Playfair_Display, 10))
        self.citation_label.setStyleSheet("""
            color: #E8E8E8;
            line-height: 1.7;
            font-weight: 300;
            padding: 5px;
        """)

        # Разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.25);
            max-height: 1px;
            margin: 2px 20px;
        """)
        separator.setFixedHeight(2)

        # Автор цитаты
        self.citation_author_label = QLabel()
        self.citation_author_label.setText(author_text)
        self.citation_author_label.setWordWrap(True)
        self.citation_author_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        if len(author_text) < 40:
            self.citation_author_label.setFont(QFont(self.font_family_Inter, 12))
        elif len(author_text) < 80:
            self.citation_author_label.setFont(QFont(self.font_family_Inter, 10))
        elif len(author_text) > 120:
            self.citation_author_label.setFont(QFont(self.font_family_Inter, 6))
        else:
            self.citation_author_label.setFont(QFont(self.font_family_Inter, 8))
        self.citation_author_label.setStyleSheet("""
            color: #42A5F5;
            font-weight: 400;
            letter-spacing: 0.3px;
            opacity: 0.9;
            padding: 7px;
        """)
        self.citation_author_label.setMinimumHeight(20)
        self.citation_author_label.setMaximumHeight(50)

        self.citation_layout.addWidget(self.citation_label)
        self.citation_layout.addWidget(separator)
        self.citation_layout.addWidget(self.citation_author_label)

        self.citation.setLayout(self.citation_layout)

        # Прогрессбар
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #3C3F41;
                border: none;
                border-radius: 4px;
                height: 8px;
                text-align: center;
                color: white;
                font-size: 10px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #2196F3,
                    stop: 0.5 #42A5F5,
                    stop: 1 #1E88E5
                );
                border-radius: 4px;
                margin: 1px;
            }
        """)
        self.progress_bar.setFixedSize(360,17)
        self.progress_bar.move(10,475)

        self.timer_animation = QTimer()
        self.timer_animation.timeout.connect(self.update_animation)
        self.timer_animation.start(35)

        self.background_window_by_time_of_day()

        animationAppearanceWindow(self, duration = 700)

        debug_log("[I] запуск таймера на 3 секунды, после чего окна закроется")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_closing)
        self.timer.start(5000)

        center_window(self)

    def get_random_image_from_folder(self, folder_path: str) -> str:
        """
        Возвращает путь к случайному изображению из указанной папки
        :param folder_path: путь к папке с изображениями
        :return: путь к случайному изображению
        """
        folder = Path(folder_path)

        # Проверяем, существует ли папка
        if not folder.exists():
            warning_log(f"[W] Папка не найдена: {folder_path}")
            return ""

        image_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
        images = [f for f in folder.iterdir() if f.suffix.lower() in image_extensions]

        if not images:
            warning_log(f"[W] В папке нет изображений: {folder_path}")
            return ""

        random_image = random.choice(images)
        debug_log(f"[I] Выбрано случайное изображение: {random_image.name}")

        return str(random_image)

    def getCitationWithAuthor(self):
        """
        Возвращает случайную цитату и её автора вместе
        """

        citation = random.choice(list(QUOTES.keys()))
        author = QUOTES[citation]
        debug_log(f"[I] Цитата: {citation}")
        debug_log(f"[I] Автор цитаты: {author}")
        return citation, author

    def update_animation(self):
        """
        Функция для обновления прогресса прогрессбара
        :return:
        """

        if self.progress_bar.value() < 100:
            self.progress_bar.setValue(self.progress_bar.value() + 1)
        else:
            self.progress_bar.setValue(100)

    def start_closing(self) -> None:
        """
        Запускает анимацию исчезания и закрытия окна
        """
        debug_log("[I] запуск анимации исчезания окна")
        animationDindisappearanceAndClosing(self, duration=1000)

    def background_window_by_time_of_day(self) -> None:
        """
        Функция для смены фона загрузочного окна на то, что соответствует времени суток.
        :return:
        """

        # current_hour = datetime.now().hour
        current_hour = 23 # - отладка и тестирование

        debug_log(f"[I] текущее время {current_hour}")

        debug_log("[I] вывод приветствия в соответствии с текущим времени")

        if 6 <= current_hour < 11:
            self.lb_hi_prog.setText("Доброе утро!")
            folder_path = "resources/images/for_start_window/images/morning"


        elif 11 <= current_hour < 17:
            self.lb_hi_prog.setText("Добрый день")
            folder_path = "resources/images/for_start_window/images/day"

        elif 17 <= current_hour < 21:
            self.lb_hi_prog.setText("Добрый вечер")
            folder_path = "resources/images/for_start_window/images/evening"

        else:
            self.lb_hi_prog.setText("Доброй ночи")
            folder_path = "resources/images/for_start_window/images/night"

        img_path = self.get_random_image_from_folder(folder_path)
        path_bg_loading = Path(f'{img_path}')
        self.loading_window.setStyleSheet(
            f"background-image: url({path_bg_loading.as_posix()}); border-radius: 10px;")

        # главный цвет изображения
        main_color = getMainColorImage(img_path)
        self.lb_hi_prog.setStyleSheet(f"font-weight: bold; color: rgb{main_color}")

        r, g, b = main_color

        # Создаём градиент от цвета изображения к тёмному фону
        self.widget_gradient.setStyleSheet(f"""
                background: qlineargradient(
                    x1: 0, y1: 1, x2: 1, y2: 0,
                    stop: 0 rgba({r}, {g}, {b}, 0.0),    /* снизу — цвет изображения (прозрачный) */
                    stop: 0.6 rgba({r}, {g}, {b}, 0.15), /* середина — лёгкий оттенок */
                    stop: 1 rgba({r}, {g}, {b}, 0.3)     /* сверху — цвет изображения (полупрозрачный) */
                );
                border-radius: 10px;
            """)

    def mousePressEvent(self, event) -> None:
        """
        обработчик события нажатия кнопки мыши. self - ссылка на текущий объект,
         event - объект события, содержащий информацию о нажатии
        (какая кнопка, координаты и т.д.).
        """

        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint()
            event.accept()


    def mouseMoveEvent(self, event) -> None:
        """
        обработчик события движения мыши. self - ссылка на текущий объект,
         event	- объект события, содержащий информацию о движении
        (координаты, кнопки)
        """

        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.drag_position
            self.move(self.pos() + delta)
            self.drag_position = event.globalPosition().toPoint()
            event.accept()
