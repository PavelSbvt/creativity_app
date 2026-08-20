import json
from pathlib import Path

from utils.output_rich import simple_log, debug_log, warning_log, success_log, log_error


class SettingsManager:
    """
    Класс для работы с настройками
    """

    def __init__(self):
        self.config_path = Path("config/settings.json")
        self.settings = {}

    def write_standard_settings(self):
        with open(self.config_path, "w", encoding="utf-8") as json_file:
            # Стандартные настройки
            data = {
                "app_name": "Creativity",
                "version": "0.3.9",
                "loading_window_timer": 5000
            }
            json.dump(data, json_file, ensure_ascii=False, indent=4)
            debug_log("[I] Применены стандартные настройки")

    def write_settings(self):
        """
        Записывает настройки в JSON-файл
        """

        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        self.write_standard_settings()

        success_log(f"[I] Файл сохранён: {self.config_path}")

    def read_settings(self):
        """
        Читает настройки из JSON-файла
        """

        if not self.config_path.exists():
            warning_log(f"[W] Файл не найден: {self.config_path}")
            return {}

        with open(self.config_path, 'r', encoding='utf-8') as file:
            settings_data = json.load(file)
            # print(settings_data)

            success_log("[I] Настройки получены")
            return settings_data

    def get_settings(self):
        """
        Функция для инициализации проверки файла настроек (проверка наличия данных и их заполнение
         в случае необходимости).
        :return:
        """
        if not self.config_path.exists():
            warning_log(f"[W] Файл не найден: {self.config_path}")
            self.write_settings()
            debug_log("Принудительно записаны стандартные настройки")

        try:
            settings_data = self.read_settings()

            app_name = settings_data.get("app_name", "Неизвестно")
            simple_log(f"Название приложения: {app_name}")

            app_version = settings_data.get('version', 'неизвестно')
            simple_log(f"Версия: {app_version}")

        except json.JSONDecodeError as e:
            warning_log(f"[W] Ошибка открытия json файла с настройками: {e}")

            with open(self.config_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                if not content:
                    warning_log("Файл с настройками пуст")

                    self.write_standard_settings()
                else:
                    with open(self.config_path, "w", encoding="utf-8") as file:
                        file.write("")
                    self.write_standard_settings()

if __name__ == "__main__":
    settings_test = SettingsManager()
    settings_test.get_settings()
