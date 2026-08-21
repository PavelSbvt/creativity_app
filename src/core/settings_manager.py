import json
from pathlib import Path

from utils.output_rich import simple_log, debug_log, warning_log, success_log, log_error


class SettingsManager:
    """
    Класс для работы с настройками программы.
    """

    def __init__(self):
        self.config_path = Path("config/settings.json")
        self.settings = {}

        self.app_name = "Creativity"
        self.app_version = "0.3.9"
        self.loading_window_timer_duration = 5000

        self.get_settings()

    def write_standard_settings(self) -> None:
        """
        Функция для записи стандартных настроек в файл (по пути сохранения настроек - self.config_path).

        :return: None.
        """

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
        Записывает стандартные настройки в JSON-файл, создаёт родительскую папку и файл
        по пути файла из атрибута класса настроек - self.config_path.

        :return: None.
        """

        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        self.write_standard_settings()

        success_log(f"[I] Файл сохранён: {self.config_path}")

    def read_settings(self) -> None:
        """
        Читает настройки из JSON-файла

        :return: None.
        """

        if not self.config_path.exists():
            warning_log(f"[W] Файл с настройками не найден: {self.config_path}")
            return {}

        with open(self.config_path, 'r', encoding='utf-8') as file:
            settings_data = json.load(file)
            # print(settings_data)

            success_log("[I] Настройки получены")
            return settings_data

    def rewrite_settings(self) -> None:
        """
        Функция для перезаписи файла с настройками.

        Заполнит файл с настройками данными атрибутов класса.

        :return: None.
        """

        with open(self.config_path, "w", encoding="utf-8") as file:
            debug_log("[debug] Очистка файла с настройками (перезапись).")
            file.write("")
        self.write_standard_settings()
        debug_log("[debug] Настройки обновлены.")

    def get_settings(self) -> None:
        """
        Функция для инициализации проверки файла настроек (проверка наличия данных и
        их заполнение в случае необходимости).

        Читает файл с настройками, если это возможно, или заполняет стандартные настройки в файл.
        Обновляет атрибуты класса теми, которые найдет в файле с настройками.

        :return: None.
        """

        if not self.config_path.exists():
            warning_log(f"[W] Файл с настройками не найден: {self.config_path}")
            self.write_settings()
            debug_log("Принудительно записаны стандартные настройки")

        try:
            settings_data = self.read_settings()

            app_name = settings_data.get("app_name", "Неизвестно")
            self.app_name = app_name

            app_version = settings_data.get('version', 'неизвестно')
            self.app_version = app_version

            loading_window_timer_duration = settings_data.get("loading_window_timer", "Неизвестно")
            self.loading_window_timer_duration = loading_window_timer_duration

        except json.JSONDecodeError as e:
            warning_log(f"[W] Ошибка открытия json файла с настройками. Текст ошибки: {e}")

            with open(self.config_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                if not content:
                    # Если файл с настройками пуст, то записать стандартные настройки.
                    warning_log("[W] Файл с настройками пуст")

                    self.write_standard_settings()
                else:
                    # Если файл с настройками битый, то переписать.
                    self.rewrite_settings()

    def print_settings(self) -> None:
        """
        Функция для вывода настроек (при запуске программы в лог)

        Только вывод в лог.
        :return: None.
        """

        simple_log(f"Название приложения: {self.app_name}")
        simple_log(f"Версия: {self.app_version}")
        simple_log(f"Время работы таймера показа загрузочного окна: {self.loading_window_timer_duration}")

    def set_app_name_settings(self, app_name: str):
        """
        Функция для задания нового имени приложения.
        Перепишет настройки на новое значение.

        Атрибут класса настроек (self.app_name) получает новое значение.

        :param app_name: Принимается новое имя приложения

        :return: None.
        """

        debug_log(f"Имя приложения изменено с {self.app_name} на {app_name}")
        self.app_name = app_name
        self.rewrite_settings()

    def get_app_name(self) -> str:
        """
        Функция для получения имени приложения.

        Вернёт значение атрибута класса настроек (имени приложения - self.app_name).

        :return: Str(self.app_name).
        """

        app_name =self.app_name
        return app_name

    def set_loading_window_timer_duration(self, loading_window_timer_duration: int):
        """
        Функция для задания нового значения таймера загрузочного окна приложения.
        Перепишет настройки на новое значение.

        Атрибут класса настроек (self.loading_window_timer_duration) получает новое значение.

        :param loading_window_timer_duration: Принимается новое значения таймера загрузочного окна приложения

        :return: None.
        """

        debug_log(f"Время работы таймера загрузочного окна изменено с {self.loading_window_timer_duration} на {loading_window_timer_duration}")
        self.loading_window_timer_duration = loading_window_timer_duration
        self.rewrite_settings()

    def get_loading_window_timer_duration(self):
        """
        Функция для получения значения таймера загрузочного окна приложения.

        Вернёт значение атрибута класса настроек
        (значение таймера загрузочного окна приложения - self.loading_window_timer_duration).

        :return: Int(self.loading_window_timer_duration).
        """

        loading_window_timer_duration =self.loading_window_timer_duration
        return loading_window_timer_duration

    def set_app_version(self, version: str):
        """
        Функция для задания параметру версии приложения нового значения.
        Перепишет настройки на новое значение.

        Атрибут класса настроек (self.app_version) получает новое значение.

        :param version: Принимается новое значения параметра версии приложения.

        :return: None.
        """

        debug_log(
        f"Версия приложения изменена с {self.app_version} на {version}")
        self.app_version = version
        self.rewrite_settings()

    def get_app_version(self):
        """
        Функция для получения версии приложения.

        Вернёт значение атрибута класса настроек
        (значение версии приложения - self.app_version).

        :return: Str(app_version).
        """

        app_version = self.app_version
        return app_version

settings = SettingsManager()

if __name__ == "__main__":
    settings_test = SettingsManager()
    settings_test.get_settings()
