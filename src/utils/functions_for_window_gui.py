import colorsys

from PIL import Image

from utils.output_rich import simple_log, debug_log, log_error


def center_window(self) -> None:
    """
    функция для центрирования главного окна, чтобы оно появлялось
    по центру экрана пользователя после исчезновения загрузочного окна
    """

    qr = self.frameGeometry()
    cp = self.screen().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())

def getMainColorImage(image_path: str):
    try:
        img = Image.open(image_path)
        img = img.resize((1, 1))
        r, g, b = img.getpixel((0, 0))

        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        s = max(0.6, min(1.0, s * 1.6))
        v = max(0.5, min(1.0, v * 1.4))
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        r, g, b = int(r * 255), int(g * 255), int(b * 255)

        brightness = (r + g + b) / 3
        max_diff = max(abs(r - g), abs(r - b), abs(g - b))

        if brightness < 100 or max_diff < 50:
            debug_log(f"[I] Цвет недостаточно яркий")

            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            s = max(0.8, min(1.0, s * 2.0))
            v = max(0.7, min(1.0, v * 1.6))
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            r, g, b = int(r * 255), int(g * 255), int(b * 255)

            brightness2 = (r + g + b) / 3
            max_diff2 = max(abs(r - g), abs(r - b), abs(g - b))

            if brightness2 < 80 or max_diff2 < 40:
                debug_log(f"[I] Не удалось извлечь главный цвет изображения - малая яркость (яркость: {brightness2:.0f})")

                return (220, 220, 220)

            debug_log(f"усиленный цвет: rgb({r}, {g}, {b})")
            return (r, g, b)

        debug_log(f"главный цвет изображения: rgb({r}, {g}, {b})")
        return (r, g, b)

    except Exception as e:
        log_error(f"[E] Ошибка: {e}")
        return (220, 220, 220)
