from flask import redirect, url_for, render_template

from application import conf, app


"""Файл запуска приложения/файл маршрутов."""

# ------- Маршруты приложения ------------------------------------------

@app.route("/")
@app.route("home")
def home():
    # TODO Проверка авторизации.
    if True:
        return render_template("admin.html")
    else:
        return render_template("login.html")


@app.route("login")
def login():
    # TODO Форма авторизации.
    return redirect(url_for("login.html"))


@app.route("logout")
def logout():
    # TODO Выход из пользователя.
    pass


# ------- Маршруты API -------------------------------------------------

# TODO Получение информации о состоянии интерфейса.
# TODO Включение/выключение интерфейса.
# TODO Добавление/удаление адреса.
# TODO Изменение адреса.
# TODO Изменение маски.