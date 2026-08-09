from pathlib import Path

from PyQt6.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea,
QLabel)
from PyQt6.QtCore import Qt, QPoint, QEvent
from PyQt6.QtGui import QResizeEvent, QPixmap

from utils.functions_for_main_window_gui import center_window
from core.users_notes import notes, Note, createNote, createNewNoteWindow, updateFlag
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

        # Шапка
        self.cap_widget = QWidget()
        self.cap_widget.setStyleSheet("""
                    background-color: orange;
                    border-bottom: 2px solid #e67e22;
                """)
        self.cap_widget.setFixedHeight(55)

        # Основной контент
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: gray;")

        main_layout.addWidget(self.cap_widget)
        main_layout.addWidget(self.content_widget)

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
        scroll_widget.setStyleSheet("background-color: #f5f5f5;")

        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.setContentsMargins(20, 20, 20, 20)

        # Создал объекты вручную (для теста)
        note_1 = Note("title", "elephant")
        note_2 = Note("raw", "raw - format of photoes")
        note_3 = Note("", "")

        self.show_notes_in_gui(self.scroll_layout)

        scroll_widget.setLayout(self.scroll_layout)
        scroll_area.setWidget(scroll_widget)

        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

        # кнопка закрытия основного окна приложения.
        self.button_close = QPushButton(self)
        self.button_close.setFixedSize(45, 45)
        self.button_close.move(750, 5)
        self.button_close.setCursor(Qt.CursorShape.PointingHandCursor)
        close_button_path = Path("resources/images/main_window/icons/close_icon.png")
        self.button_close.setStyleSheet(f"""
                            background-image:url({close_button_path.as_posix()});
                            background-color: transparent;
                            border: none;
                            background-repeat: no-repeat;
                            background-position: center;
                            """)
        self.button_close.clicked.connect(self.close_func)

        # Кнопка создания записи
        self.button_create_note = QPushButton(self)
        self.button_create_note.setFixedSize(55,55)
        self.button_create_note.move(730,530)
        self.button_create_note.setCursor(Qt.CursorShape.PointingHandCursor)
        button_create_path = Path("resources/images/main_window/icons/button_create_new_note.png")
        self.button_create_note.setStyleSheet(f"""
                            background-image:url({button_create_path.as_posix()});
                            background-color: transparent;
                            border: none;
                            background-repeat: no-repeat;
                            background-position: center;
                            """)
        self.button_create_note.clicked.connect(self.createNewNote)

        center_window(self)

        self.count_notes = len(notes)

        # Кнопка обновления gui
        self.button_update = QPushButton(self)
        self.button_update.setStyleSheet("""
                    QPushButton {
                        background-color: white;
                        color: black;
                        font: bold;
                        font-size: 16px;
                        border: none;
                        border-radius: 17px;
                    }
                    QPushButton:hover {
                        background-color: gray;
                    }
                    QPushButton:pressed {
                        background-color: black;
                    }
        """)
        self.button_update.setFixedSize(35,35)
        self.button_update.move(5,5)

        self.button_update.clicked.connect(self.refresh_notes_display)

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
        for note in notes:
            widget = QWidget()
            widget.setStyleSheet(f"""
                background-color: {'#FF6B6B' if note.id % 2 == 0 else '#4ECDC4'};
                border-radius: 8px;
            """)

            if not note.title and note.content:
                widget.setFixedHeight(80)
            elif note.title and not note.content:
                widget.setFixedHeight(80)
            elif not note.content and not note.content:
                widget.setFixedHeight(80)
            else:
                widget.setFixedHeight(120)

            # Горизонтальный layout
            main_widget_layout = QHBoxLayout()
            main_widget_layout.setSpacing(15)
            main_widget_layout.setContentsMargins(10, 10, 10, 10)

            if note.image_path and Path(note.image_path).exists():
                widget.setFixedHeight(520)
                image_label = QLabel()
                pixmap = QPixmap(note.image_path)
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(
                        450, 450,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    image_label.setPixmap(scaled_pixmap)
                    image_label.setFixedSize(450, 450)
                    image_label.setStyleSheet("border-radius: 5px;")
                    main_widget_layout.addWidget(image_label)

            # Вертикальный layout для текста
            text_layout = QVBoxLayout()
            text_layout.setSpacing(5)

            # label_number_note = QLabel(f"Заметка {note.id}")
            # label_number_note.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
            # label_number_note.setAlignment(Qt.AlignmentFlag.AlignLeft)

            label_title_note = QLabel(note.title if note.title else "")
            label_title_note.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
            label_title_note.setAlignment(Qt.AlignmentFlag.AlignLeft)

            label_content_note = QLabel(note.content if note.content else "")
            label_content_note.setStyleSheet("color: white; font-size: 14px;")
            label_content_note.setAlignment(Qt.AlignmentFlag.AlignLeft)
            label_content_note.setWordWrap(True)

            # text_layout.addWidget(label_number_note)
            text_layout.addWidget(label_title_note)
            text_layout.addWidget(label_content_note)

            main_widget_layout.addLayout(text_layout)
            main_widget_layout.addStretch()

            widget.setLayout(main_widget_layout)
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
