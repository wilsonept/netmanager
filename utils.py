from asyncio import subprocess


import subprocess
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
    
        conf["iface"] = get_iface()
    
    return True


# TODO Получение основного интерфейса.
def get_iface():
    """Определяет основной интерфейс по дефолтному маршруту."""
    args = ["ip", "-o", "-4", "route", "show", "to", "default"]
    sproc = subprocess.run(args, capture_output=True)
    if sproc.stderr:
        raise Exception(sproc.stderr)

    route = sproc.stdout.decode("utf8")
    iface = route.split()[-1]
    if iface:
        return iface

    raise Exception("Не удалось определить основной интерфейс, укажите его в config.json вручную.")

# TODO Получение информации о состоянии интерфейса.
def get_iface_cidrs():
    """Возвращает список CIDR адресов на интерфейсе."""
    args = ["ip", "-o", "-4", "addr", "show", "dev", conf['iface']]
    sproc = subprocess.run(args, capture_output=True)
    if sproc.stderr:
        raise Exception(sproc.stderr)

    sout = sproc.stdout.decode("utf8").replace("\s+"," ").strip().split("\n")
    result = [s.split()[3] for s in sout]
    if result:
        return result

    raise Exception("")

# TODO Включение/выключение интерфейса.
# TODO Добавление/удаление адреса.
# TODO Изменение адреса.
# TODO Изменение маски.


if __name__ == "__main__":
    
    print("==== Самотестирование", __file__, "====")

    conf = load_json("./config.json")
    print(f"\n{validate_conf.__name__}:", validate_conf(conf))
    
    print(f"\n{get_iface.__name__}:", get_iface())

    print(f"\n{validate_conf.__name__}:", validate_conf(conf))

    print(f"\n{get_iface_cidrs.__name__}", get_iface_cidrs())
    