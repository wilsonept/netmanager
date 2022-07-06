from flask import Flask

from utils import load_json, validate_conf

"""Файл конфигурации приложения."""


conf = load_json("config.json")

if validate_conf(conf):
    app = Flask(__name__)
    app.config["SECRET_KEY"]=conf["app_secret"]
