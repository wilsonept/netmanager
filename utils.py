import json

"""
Файл с вспомогательными функциями.
"""


def load_json(json_file: str):
    """Возвращает данные из json файла."""
    with open(json_file, "r") as f:
        json_data = json.load(f)
        return json_data

def validate_conf(conf) -> bool:
    """Валидирует необходимые поля файла конфигурации."""

    # Проверяем поле app_secret
    if "app_secret" in conf.keys() and conf["app_secret"]:
        pass
    else:
        print("В файле конфигурации не указан секретный ключ приложения.",
              "\nУкажите его и повторите попытку.")
        return False

    # Проверяем поле iface
    if not "iface" in conf.keys():
        print("В файле конфигурации не указан управляемый интерфейс",
            "\nОн будет выбран по основному маршруту.")
    
    return True


# TODO Получение информации о состоянии интерфейса.
# TODO Включение/выключение интерфейса.
# TODO Добавление/удаление адреса.
# TODO Изменение адреса.
# TODO Изменение маски.


if __name__ == "__main__":
    
    conf = load_json("./config.json")
    validate_conf(conf)