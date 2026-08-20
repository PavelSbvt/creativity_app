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

        self.app_name = "Creativity"
        self.app_version = "0.3.9"
        self.loading_window_timer_duration = 5000

    def write_standard_settings(self):
        with open(self.config_path, "w", encoding="utf-8") as json_file:
            # Стандартные настройки
            data = {
                "app_name": self.app_name,
                "version": self.app_version,
                "loading_window_timer": self.loading_window_timer_duration
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
            warning_log(f"[W] Файл с настройками не найден: {self.config_path}")
            return {}

        with open(self.config_path, 'r', encoding='utf-8') as file:
            settings_data = json.load(file)
            # print(settings_data)

            success_log("[I] Настройки получены")
            return settings_data

    def rewrite_settings(self):
        with open(self.config_path, "w", encoding="utf-8") as file:
            debug_log("[debug] Очистка файла с настройками (перезапись).")
            file.write("")
        self.write_standard_settings()
        debug_log("[debug] Настройки обновлены.")

    def get_settings(self):
        """
        Функция для инициализации проверки файла настроек (проверка наличия данных и их заполнение
         в случае необходимости).
        :return:
        """
        if not self.config_path.exists():
            warning_log(f"[W] Файл с настройками не найден: {self.config_path}")
            self.write_settings()
            debug_log("Принудительно записаны стандартные настройки")

        try:
            settings_data = self.read_settings()

            app_name = settings_data.get("app_name", "Неизвестно")
            simple_log(f"Название приложения: {app_name}")

            app_version = settings_data.get('version', 'неизвестно')
            simple_log(f"Версия: {app_version}")

            loading_window_timer_duration = settings_data.get("loading_window_timer", "Неизвестно")
            simple_log(f"Время работы таймера показа загрузочного окна: {loading_window_timer_duration}")

        except json.JSONDecodeError as e:
            warning_log(f"[W] Ошибка открытия json файла с настройками. Текст ошибки: {e}")

            with open(self.config_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                if not content:
                    warning_log("[W] Файл с настройками пуст")

                    self.write_standard_settings()
                else:
                    self.rewrite_settings()

    def change_app_name_settings(self, app_name):
        debug_log(f"Имя приложения изменено с {self.app_name} на {app_name}")
        self.app_name = app_name
        self.rewrite_settings()

    def get_app_name(self):
        app_name =self.app_name
        return app_name

    def change_loading_window_timer_duration(self, loading_window_timer_duration):
        debug_log(f"Время работы таймера загрузочного окна изменено с {self.loading_window_timer_duration} на {loading_window_timer_duration}")
        self.loading_window_timer_duration = loading_window_timer_duration
        self.rewrite_settings()

    def get_loading_window_timer_duration(self):
        loading_window_timer_duration =self.loading_window_timer_duration
        return loading_window_timer_duration

settings = SettingsManager()

if __name__ == "__main__":
    settings_test = SettingsManager()
    settings_test.get_settings()
