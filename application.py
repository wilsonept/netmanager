import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from utils import load_json, validate_conf

"""Файл конфигурации приложения."""


def create_app(conf):
    global DB

    app = Flask(__name__)
    app.config["SECRET_KEY"]=conf["app_secret"]

    # Подключение к БД.
    db_file_path = os.path.join(conf["db_folder_path"],
                                f"{conf['db_name']}.db")
    engine = f"sqlite:///{db_file_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = engine

    # Инициализация БД.
    DB = SQLAlchemy(app)

    return app


conf = load_json("config.json")

if validate_conf(conf):
    app = create_app(conf)


if __name__ == "__main__":
    print("URI подключения:", app.config["SQLALCHEMY_DATABASE_URI"])
