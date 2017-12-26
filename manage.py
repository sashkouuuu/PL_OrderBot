from flask import Flask, url_for
from flask_sslify import SSLify
from flask import request

import telebot
from telebot import types

import config
from admin_board import admin
from user_board import user

app = Flask(__name__)
sslify = SSLify(app)

app.register_blueprint(user)
app.register_blueprint(admin)





if __name__ == '__main__':
    app.run()