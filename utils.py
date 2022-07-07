import subprocess
import json
import os

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
    
    # Проверяем поле gateway
    if not "gateway" in conf.keys():
        print("В файле конфигурации не указан основной шлюз.",
            "\nОн будет выбран по основному маршруту.")
    
        conf["gateway"] = get_gateway(conf["iface"])

    return True


# Получение основного интерфейса.
def get_iface():
    """Определяет основной интерфейс по дефолтному маршруту."""
    args = ["ip", "-o", "-4", "route", "show", "to", "default"]
    sproc = subprocess.run(args, capture_output=True)
    if sproc.stderr:
        raise Exception(sproc.stderr)

    route = sproc.stdout.decode("utf8")
    if route:
        iface = route.split()[-1]
        return iface

    raise Exception("Не удалось определить основной интерфейс, укажите его в config.json вручную.")

# Получение информации о состоянии интерфейса.
def get_iface_cidrs(iface) -> list:
    """Возвращает список CIDR адресов на интерфейсе."""
    args = ["ip", "-o", "-4", "addr", "show", "dev", iface]
    sproc = subprocess.run(args, capture_output=True)
    if sproc.stderr:
        raise Exception(sproc.stderr)

    sout = sproc.stdout.decode("utf8").replace("\s+"," ").strip().split("\n")
    result = [s.split()[3] for s in sout if s]
    if result:
        return result

# Получаем адрес роутера.
def get_gateway(iface: str):
    """Получает ip адрес шлюза"""
    args = ["ip", "-o", "-4", "route", "show", "to", "default"]
    sproc = subprocess.run(args, capture_output=True)
    if sproc.stderr:
        raise Exception(sproc.stderr)

    if len(sproc.stdout.split()) >= 2:
        gate = sproc.stdout.split()[2].decode("utf8")
        return gate

# Включение/выключение интерфейса.
def set_iface_link(iface: str, state: str):
    """
    Функция включения/отключения интерфейса.
    Принимает:
      :str:`iface` - название интерфейса.
      :str:`state` - состояние 'up' или 'down'
    """
    if not state in ("up", "down"):
        raise Exception("Параметр state указан не верно, используйте 'up' или 'down'")

    gate = conf["gateway"] if conf["gateway"] else ""

    # Включаем или отключаем интерфейс.
    ip_link_sh = os.getcwd() + "/scripts/" + "ip_link.sh"
    args = ["sudo", ip_link_sh, iface, state, gate]
    sproc_link = subprocess.run(args, capture_output=True)
    if sproc_link.stderr:
        raise Exception(sproc_link.stderr)
    
    return get_iface_cidrs(iface)
    
    
# Добавление/удаление адреса.
def set_iface_ip(iface: str, action: str, addr: str, mask: str):
    """
    Функция добавления/удаления интерфейса.
    Принимает:
      :str:`iface` - название интерфейса.
      :str:`action` - действие 'del' или 'add'.
      :str:`addr` - ip адрес.
      :str:`mask` - маска от 1 до 24.
    """

    if not action in ("del", "add"):
        raise Exception("Параметр action указан не верно, используйте 'up' или 'down'")

    gate = conf["gateway"] if conf["gateway"] else ""

    # Добавляем/удаляем ip адрес.
    ip_addr_sh = os.getcwd() + "/scripts/" + "ip_addr.sh"
    args = ["sudo", ip_addr_sh, iface, action, addr, mask, gate]
    sproc_link = subprocess.run(args, capture_output=True)
    if sproc_link.stderr:
        raise Exception(sproc_link.stderr)
    
    return get_iface_cidrs(iface)

# TODO Изменение адреса/маски.
def set_iface_ip_mask(iface: str, old_addr: str, old_mask,
                      addr: str, mask: str):
    """
    Изменяет указанный ip и маску на указанном интерфейсе
    путем пересоздания адреса интерфейса.
    """

    # Удаляет указанный CIDR адрес.
    set_iface_ip(iface, "del", old_addr, old_mask)

    # Добавляет указанный CIDR адрес.
    set_iface_ip(iface, "add", addr, mask)

    return get_iface_cidrs(iface)


if __name__ == "__main__":
    
    print("==== Самотестирование", __file__, "====")

    # Валидация конфига.
    conf = load_json("./config.json")
    print(f"\n{validate_conf.__name__}:", validate_conf(conf))
    
    # Получение интерфейса и повторная валидация конфига.
    if not conf["iface"]:
        print(f"\n{get_iface.__name__}:", get_iface())
        print(f"\n{validate_conf.__name__}:", validate_conf(conf))

    # Получение списка адресов на интерфейсе.
    print(f"\n{get_iface_cidrs.__name__}", get_iface_cidrs(conf["iface"]))
    
    # Включение/отключение интерфейса.
    print(f"\n{set_iface_link.__name__}", set_iface_link(conf["iface"], "down"))
    print(f"\n{set_iface_link.__name__}", set_iface_link(conf["iface"], "up"))
    
    # Добавление/удаление ip адреса.
    print(f"\n{set_iface_ip.__name__}",
          set_iface_ip(conf["iface"], "del", "10.0.0.0", "24"))

    print(f"\n{set_iface_ip.__name__}",
          set_iface_ip(conf["iface"], "add", "10.0.0.0", "24"))

    # Изменение адреса/маски.
    print(f"\n{set_iface_ip_mask.__name__}",
          set_iface_ip_mask(conf["iface"], "10.0.0.0", "24", "10.1.1.1", "24")
    )

    print(f"\n{set_iface_ip_mask.__name__}",
          set_iface_ip_mask(conf["iface"], "10.1.1.1", "24", "10.0.0.0", "24")
    )