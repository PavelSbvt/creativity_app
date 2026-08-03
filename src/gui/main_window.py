from pathlib import Path

from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QResizeEvent

from utils.functions_for_main_window_gui import center_window


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

        scroll_layout = QVBoxLayout()
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_layout.setSpacing(10)
        scroll_layout.setContentsMargins(20, 20, 20, 20)

        for i in range(20):
            widget = QWidget()
            widget.setStyleSheet(f"""
                        background-color: {'#FF6B6B' if i % 2 == 0 else '#4ECDC4'};
                        border-radius: 8px;
                    """)
            widget.setFixedHeight(60)

            from PyQt6.QtWidgets import QLabel
            label = QLabel(f"Элемент {i + 1}")
            label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            widget_layout = QVBoxLayout()
            widget_layout.addWidget(label)
            widget.setLayout(widget_layout)

            scroll_layout.addWidget(widget)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

        # кнопка закрытия основного окна приложения.
        button_close = QPushButton(self)
        button_close.setFixedSize(45, 45)
        button_close.move(750, 5)
        button_close.setCursor(Qt.CursorShape.PointingHandCursor)
        close_button_path = Path("resources/images/main_window/icons/close_icon.png")
        button_close.setStyleSheet(f"""
                            background-image:url({close_button_path.as_posix()});
                            background-color: transparent;
                            border: none;
                            background-repeat: no-repeat;
                            background-position: center;
                            """)
        button_close.clicked.connect(self.close)

        center_window(self)

    def resizeEvent(self, event: QResizeEvent):
        """
        Обработчик изменения размера окна
        """

        new_size = event.size()

        new_width = new_size.width()
        new_height = new_size.height()

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
