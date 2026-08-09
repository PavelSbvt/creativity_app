from pathlib import Path

from PyQt6.QtWidgets import (QWidget, QPushButton, QLabel, QTextEdit, QLineEdit,
                             QVBoxLayout, QFileDialog)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPixmap

from utils.output_rich import simple_log, debug_log, success_log, exit_log, warning_log


updateFlag = False

notes = []

class Note():
    """
    Класс для заметок/записей пользователя
    """

    def __init__(self, title, content, image_path = None):

        self.title = title
        self.content = content
        self.image_path = image_path

        self.id: int = len(notes) + 1

        if image_path:
            success_log(f"[I] Создана запись №{self.id} с изображением: {Path(image_path).name}")

        if len(self.title) > 0 and len(self.content) > 0:
            if len(self.title) > 30 and len(self.content) > 30:
                success_log(f"[I] Создана запись №{self.id}: {self.title[:30]}..., {self.content[:30]}...")
            elif len(self.title) > 30 and len(self.content) <= 30:
                success_log(f"[I] Создана запись №{self.id}: {self.title[:30]}..., {self.content[:30]}")
            elif len(self.title) <= 30 and len(self.content) > 30:
                success_log(f"[I] Создана запись №{self.id}: {self.title[:30]}, {self.content[:30]}...")
            else:
                success_log(f"[I] Создана запись №{self.id}: {self.title[:30]}, {self.content[:30]}")
        else:
            success_log(f"[I] Создана запись №{self.id}. Без заголовка и текста.")


        notes.append(self)

def createNote():
    simple_log("Вызвана функция создания записи")
    note_title: str = input("Заголовок <<< ")
    note_content: str = input("Текст <<< ")
    note = Note(note_title, note_content)

    return note

def showNotes():
    simple_log("Показ записей")
    if notes:
        for note in notes:
            debug_log(f"Запись №{note.id}: {note.title}, {note.content}")
    else:
        simple_log("Список записей пока пуст :(")

class createNewNoteWindow(QWidget):
    """
    Класс для окна создания новой записи
    """

    def __init__(self):
        super().__init__()
        self.drag_position: QPoint = QPoint()

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: gray;")

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

        self.setLayout(main_layout)

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
        self.button_close.clicked.connect(self.closeCreateNoteWindow)

        self.label_info = QLabel(self.content_widget)
        self.label_info.setStyleSheet("color: white; font: bold; font-size: 18px;")
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label_info.setText("Редактор записи")
        self.label_info.move(20,10)

        self.title_label = QLabel(self.content_widget)
        self.title_label.setStyleSheet("color: white; font: bold; font-size: 18px;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setText("Заголовок:")
        self.title_label.move(20, 40)

        self.title_input = QLineEdit(self.content_widget)
        self.title_input.setPlaceholderText("Напишите заголовок для своей записи...")
        self.title_input.setFixedSize(650,35)
        self.title_input.move(120,35)

        self.content_label = QLabel(self.content_widget)
        self.content_label.setStyleSheet("color: white; font: bold; font-size: 18px;")
        self.content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_label.setText("Текст:")
        self.content_label.move(20, 78)

        self.content_input = QLineEdit(self.content_widget)
        self.content_input.setPlaceholderText("Напишите текст своей записи...")
        self.content_input.setFixedSize(690, 35)
        self.content_input.move(80, 75)

        self.button_create_note = QPushButton(self.content_widget)
        self.button_create_note.setStyleSheet("""
                    QPushButton {
                        background-color: white;
                        color: black;
                        font: bold;
                        font-size: 16px;
                        border: none;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: gray;
                    }
                    QPushButton:pressed {
                        background-color: black;
                    }
        """)
        self.button_create_note.setFixedSize(150, 40)
        self.button_create_note.setText("Создать запись")
        self.button_create_note.move(630,490)

        self.button_create_note.clicked.connect(self.createNoteOnPressButton)

        self.selected_image_path = None

        # Кнопка выбора изображения
        self.button_choose_image = QPushButton(self.content_widget)
        self.button_choose_image.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font: bold 14px;
                border: none;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.button_choose_image.setFixedSize(150,35)
        self.button_choose_image.setText("Прикрепить фото")
        self.button_choose_image.move(120,120)
        self.button_choose_image.clicked.connect(self.selectImage)

        # Label для отображения миниатюры
        self.image_preview = QLabel(self.content_widget)
        self.image_preview.setFixedSize(150, 150)
        self.image_preview.move(320, 120)
        self.image_preview.setStyleSheet("""
                    border: 2px dashed white;
                    border-radius: 8px;
                    background-color: rgba(255,255,255,0.1);
                """)
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview.setText("Нет\nизображения")
        self.image_preview.setWordWrap(True)

    def selectImage(self):
        """
        Открывает диалог выбора изображения
        """

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Изображения (*.png *.jpg *.jpeg *.gif)"
        )

        if file_path:
            self.selected_image_path = file_path

            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    150, 150,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_preview.setPixmap(scaled_pixmap)
                self.image_preview.setText("")
                debug_log(f"[I] Выбрано изображение: {Path(file_path).name}")
            else:
                warning_log("[W] Не удалось загрузить изображение")

    def createNoteOnPressButton(self):
        """
        Функция для создания новой заметки/записи
        :return:
        """

        title = self.title_input.text().strip()
        content = self.content_input.text().strip()

        if not title and not content and not self.selected_image_path:
            warning_log("[W] Попытка создать пустую заметку (нет заголовка, текста и изображения)")
            return

        note = Note(title, content, self.selected_image_path)
        simple_log(f"[I] Создана запись №{note.id} по кнопке")

        self.title_input.clear()
        self.content_input.clear()
        self.image_preview.clear()

        self.image_preview.setText("Нет\nизображения")
        self.selected_image_path = None

        global updateFlag
        updateFlag = True

        self.close()

    def closeCreateNoteWindow(self):
        exit_log("[I][Exit] Выход из окна создания записи.")
        self.close()

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
