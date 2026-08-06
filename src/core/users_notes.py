from pathlib import Path

from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QTextEdit, QLineEdit
from PyQt6.QtCore import Qt, QPoint

from utils.output_rich import simple_log, debug_log, success_log, exit_log


notes = []

class Note():
    """
    Класс для заметок/записей пользователя
    """

    def __init__(self, title, content):

        self.title = title
        self.content = content

        self.id: int = len(notes) + 1

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
    def __init__(self):
        super().__init__()
        self.drag_position: QPoint = QPoint()

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: gray; border-radius: 20px;")

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

        title_label = QLabel("Заголовок:", self)
        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Введите заголовок...")

        content_label = QLabel("Содержание:", self)
        self.content_input = QTextEdit(self)
        self.content_input.setPlaceholderText("Введите текст заметки...")

        save_button = QPushButton("Сохранить", self)

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
