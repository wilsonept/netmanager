#!/bin/bash
# Добавляет/удаляет ip
# $1 - название интерфейса.
# $2 - действие "del" или "add"
# $3 - cidr адрес.
# $4 - адрес шлюза.

# Добавляем/удаляем ip
ip addr $2 $3 dev $1

# Устанавливаем дефолтный маршрут.
if [[ $4 != "" && $2 != "del" ]]; then
    ip route add default via $4
fi
