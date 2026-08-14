from pathlib import Path

from PyQt6.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea,
QLabel, QTabWidget)
from PyQt6.QtCore import Qt, QPoint, QEvent
from PyQt6.QtGui import QResizeEvent, QPixmap

from utils.functions_for_window_gui import center_window
from core.users_notes import notes, Note, createNewNoteWindow, updateFlag
from utils.output_rich import simple_log, exit_log, enter_log, debug_log


class mainWindow(QWidget):
    """
    Класс главного окна приложения
    """

    def __init__(self):
        super().__init__()

        self.drag_position: QPoint = QPoint()

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: white;")

        # Главный вертикальный layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setStyleSheet("background-color: #1A1A1A;")

        # Шапка
        self.cap_widget = QWidget()
        self.cap_widget.setStyleSheet("""
            background: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #FF8C00,
                stop: 1 #FFA726
            );
            border-bottom: 2px solid #E65100;
        """)
        self.cap_widget.setFixedHeight(55)

        # Layout для шапки
        cap_layout = QHBoxLayout()
        cap_layout.setContentsMargins(15, 5, 15, 5)
        cap_layout.setSpacing(10)

        # Название или логотип
        self.cap_title = QLabel("📷 Creativity")
        self.cap_title.setStyleSheet("""
                    color: white;
                    font-size: 18px;
                    font-weight: bold;
                    font-family: 'Playfair Display';
                """)

        # Создал объекты вручную (для теста)
        if not notes:
            note_1 = Note("title", "elephant")
            note_2 = Note("raw", "raw - format of photoes")
            note_3 = Note("", "")

        # кнопка закрытия основного окна приложения.
        self.button_close = QPushButton("✕")
        self.button_close.setFixedSize(35, 35)
        self.button_close.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_close.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 18px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(255, 0, 0, 0.5);
            }
        """)
        self.button_close.clicked.connect(self.close_func)

        # Кнопка создания записи
        self.button_create_note = QPushButton(self)
        self.button_create_note.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_create_note.setStyleSheet(f"""
                            QPushButton {{
                                background-color: rgba(255, 255, 255, 0.15);
                                color: white;
                                font-weight: bold;
                                font-size: 13px;
                                border: none;
                                border-radius: 8px;
                                padding: 6px 14px;
                            }}
                            QPushButton:hover {{
                                background-color: rgba(255, 255, 255, 0.25);
                            }}
                            QPushButton:pressed {{
                                background-color: rgba(255, 255, 255, 0.35);
                            }}
                            """)
        self.button_create_note.setText("Создать запись")
        self.button_create_note.clicked.connect(self.createNewNote)

        center_window(self)

        self.count_notes = len(notes)

        # Кнопка обновления gui
        self.button_update = QPushButton(self)
        self.button_update.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.15);
                color: white;
                font-weight: bold;
                font-size: 13px;
                border: none;
                border-radius: 8px;
                padding: 6px 14px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.25);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.35);
            }
        """)
        self.button_update.setFixedHeight(30)
        self.button_update.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_update.clicked.connect(self.refresh_notes_display)
        self.button_update.setText("Обновить")

        # Добавляем в шапку: слева заголовок, справа кнопка
        cap_layout.addWidget(self.cap_title)
        cap_layout.addStretch()
        cap_layout.addWidget(self.button_create_note)
        cap_layout.addWidget(self.button_update)
        cap_layout.addWidget(self.button_close)

        self.cap_widget.setLayout(cap_layout)

        # Таб виджет
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setStyleSheet("""
                    QTabWidget::pane {
                        background-color: #2B2B2B;
                        border: none;
                        border-radius: 8px;
                    }
                    QTabBar::tab {
                        background-color: #3C3F41;
                        color: #A9B7C6;
                        padding: 10px 20px;
                        margin-right: 4px;
                        border-top-left-radius: 8px;
                        border-top-right-radius: 8px;
                        font-size: 13px;
                        font-weight: 500;
                        font-family: 'Inter';
                        border: none;
                    }
                    QTabBar::tab:hover {
                        background-color: #4C4F51;
                        color: #FFFFFF;
                    }
                    QTabBar::tab:selected {
                        background-color: #4CAF50;
                        color: white;
                    }
                    QTabBar::tab:selected:hover {
                        background-color: #43A047;
                    }
                """)

        # Создаем страницы
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        # tab1_layout.addWidget()
        tab1.setLayout(tab1_layout)

        # ScrollArea для заметов
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
                            QScrollArea {
                                background-color: #f5f5f5;
                                border: none;
                            }
                            QScrollBar:vertical {
                                width: 8px;
                                background: #e0e0e0;
                                border-radius: 4px;
                            }
                            QScrollBar::handle:vertical {
                                background: #b0b0b0;
                                border-radius: 4px;
                            }
                            QScrollBar::handle:vertical:hover {
                                background: #909090;
                            }
                        """)

        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background-color: #2B2B2B;")

        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.setContentsMargins(20, 20, 20, 20)

        scroll_widget.setLayout(self.scroll_layout)
        scroll_area.setWidget(scroll_widget)

        tab1_layout.addWidget(scroll_area)
        tab1.setLayout(tab1_layout)

        tab2 = QWidget()
        tab2_layout = QVBoxLayout()
        tab2_layout.addWidget(QLabel("Содержимое вкладки 2"))
        tab2.setLayout(tab2_layout)

        tab3 = QWidget()
        tab3_layout = QVBoxLayout()
        tab3_layout.addWidget(QLabel("Содержимое вкладки 3"))
        tab3.setLayout(tab3_layout)

        tab4 = QWidget()
        tab4_layout = QVBoxLayout()
        tab4_layout.addWidget(QLabel("Содержимое вкладки 4"))
        tab4.setLayout(tab4_layout)

        # Добавляем вкладки
        self.tab_widget.addTab(tab1, "📋 Главная")
        self.tab_widget.addTab(tab2, "📸 Фотографии")
        self.tab_widget.addTab(tab3, "📈 Статистика")
        self.tab_widget.addTab(tab4, "⚙️ Настройки")

        main_layout.addWidget(self.cap_widget)
        main_layout.addWidget(self.tab_widget)

        self.setLayout(main_layout)

        self.show_notes_in_gui(self.scroll_layout)

    def changeEvent(self, event):
        """
        Отслеживаем изменение состояния окна
        """

        if event.type() == QEvent.Type.ActivationChange:
            if self.isActiveWindow():
                global updateFlag
                if updateFlag:
                    debug_log("[I] Обнаружено обновление заметок, обновляем GUI")
                    self.refresh_notes_display()
                    updateFlag = False
        super().changeEvent(event)

    def showEvent(self, event):
        """
        Срабатывает при показе окна
        """

        super().showEvent(event)

        global updateFlag

        if updateFlag:
            debug_log("[I] Обнаружено обновление заметок, обновляем GUI")
            self.refresh_notes_display()
            updateFlag = False

    def refresh_notes_display(self):
        """
        Полностью перерисовывает список заметок
        """

        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.show_notes_in_gui(self.scroll_layout)
        debug_log("[I] GUI обновлен")

    def close_func(self):
        """
        Функция для закрытия основного окна (срабатывает по кнопке и присылает сообщение в логе)
        :return:
        """

        exit_log("[Exit] Нажата кнопка закрытия приложения. Выход из приложения.")
        self.close()

    def createNewNote(self):
        """
        Функция для открытия редактора записей (окна редактора)
        :return:
        """

        enter_log("[Enter] Нажата кнопка создания записи. Открытие окна создания записи.")

        self.note_window = createNewNoteWindow()

        self.note_window.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.note_window.show()

    def show_notes_in_gui(self, scroll_layout):
        """
        Функция для вывода всех записей
        :param scroll_layout:
        :return:
        """

        for note in reversed(notes):

            widget = QWidget()
            widget.setStyleSheet(f"""
                background-color: {'#1B2A22' if note.id % 2 == 0 else '#1B2D2A'};
                border-radius: 8px;
            """)

            # Определяем наличие изображения
            has_image = note.image_path and Path(note.image_path).exists()
            has_title = bool(note.title)
            has_content = bool(note.content)

            # Основной вертикальный layout
            main_widget_layout = QVBoxLayout()
            main_widget_layout.setSpacing(5)
            main_widget_layout.setContentsMargins(15, 12, 15, 12)

            if has_image:
                # Контейнер для центрирования изображения
                image_container = QWidget()
                image_container_layout = QHBoxLayout()
                image_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                image_container_layout.setContentsMargins(0, 0, 0, 0)

                image_label = QLabel()
                pixmap = QPixmap(note.image_path)
                if not pixmap.isNull():
                    max_width = 720
                    max_height = 400

                    scaled_pixmap = pixmap.scaled(
                        max_width, max_height,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    image_label.setPixmap(scaled_pixmap)
                    image_label.setFixedSize(scaled_pixmap.width(), scaled_pixmap.height())
                    image_label.setStyleSheet("border-radius: 8px;")

                    image_container_layout.addWidget(image_label)
                    image_container.setLayout(image_container_layout)
                    main_widget_layout.addWidget(image_container)

            # Вертикальный layout для текста
            text_layout = QVBoxLayout()
            text_layout.setSpacing(3)

            # Заголовок (если есть)
            if has_title:
                label_title_note = QLabel(note.title)
                label_title_note.setStyleSheet("""
                    color: white; 
                    font-size: 16px; 
                    font-weight: bold;
                """)
                label_title_note.setAlignment(Qt.AlignmentFlag.AlignLeft)
                label_title_note.setWordWrap(True)
                text_layout.addWidget(label_title_note)

            if has_content:
                label_content_note = QLabel(note.content)
                label_content_note.setStyleSheet("""
                    color: white; 
                    font-size: 14px;
                """)
                label_content_note.setAlignment(Qt.AlignmentFlag.AlignLeft)
                label_content_note.setWordWrap(True)
                text_layout.addWidget(label_content_note)

            # Добавляем текст в основной layout (если есть хоть что-то)
            if has_title or has_content:
                main_widget_layout.addLayout(text_layout)

            # Добавляем растяжку ТОЛЬКО если нет изображения
            # Тогда текст будет сверху, а не по центру
            if not has_image:
                main_widget_layout.addStretch()

            widget.setLayout(main_widget_layout)

            if has_image and (has_title or has_content):
                widget.setFixedHeight(500)  # с изображением и текстом
            elif has_image and not has_title and not has_content:
                widget.setFixedHeight(420)  # только изображение (меньше высота)
            elif not has_image and (has_title or has_content):
                # без изображения - высота зависит от количества текста
                if has_title and has_content:
                    widget.setFixedHeight(110)
                else:
                    widget.setFixedHeight(80)
            else:
                widget.setFixedHeight(60)  # пустая заметка

            scroll_layout.addWidget(widget)

    def resizeEvent(self, event: QResizeEvent):
        """
        Обработчик изменения размера окна
        """

        new_size = event.size()

    def mousePressEvent(self, event) -> None:
        """
        функция, отслеживающая точку, где пользователь зажал ЛКМ
        """

        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event) -> None:
        """
        функция для вычисления смещения по изменения позиции зажатой ЛКМ.
         Перемещает окно при движении мыши с зажатой ЛКМ.
        """

        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.drag_position
            self.move(self.pos() + delta)
            self.drag_position = event.globalPosition().toPoint()
            event.accept()
