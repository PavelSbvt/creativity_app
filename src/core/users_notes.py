from utils.output_rich import simple_log, debug_log


notes = []

class Note():
    """
    Класс для заметок/записей пользователя
    """

    def __init__(self, title, content):

        self.title = title
        self.content = content

        self.id: int = len(notes) + 1

        simple_log(f"Создана запись №{self.id}: {self.title[:20]}, {self.content[:20]}")

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

showNotes()

createNote()

showNotes()
