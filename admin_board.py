from flask import Blueprint
from flask import request
from telebot import types

from user_board import bot, start

import config
import json


admin = Blueprint("admin", __name__)


def read_json():
    with open("settings", "r") as json_data:
        return json.load(json_data)


def admin_panel(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.InlineKeyboardButton(text="Категории"),
                 types.InlineKeyboardButton(text="Назад")
                 )

    msg = bot.send_message(message.chat.id,
                       "Раздел настроек бота",
                       reply_markup=keyboard)

    return bot.register_next_step_handler(msg, after_panel)


def after_panel(message, data=None):
    if message.text == "Категории" or data == "Категории":
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Добавить категорию"),
                     types.InlineKeyboardButton(text="Назад")
                     )

        data = read_json()
        for category in data["product"]:
            keyboard.add(types.InlineKeyboardButton(text=category))

        msg = bot.send_message(message.chat.id,
                               "Раздел управлением категориями",
                               reply_markup=keyboard)

        return bot.register_next_step_handler(msg, category_settings)

    elif message.text == "Назад":
        return start(message)


def category_settings(message):
    categorys = []
    data = read_json()

    for category in data["product"]:
        categorys.append(category)

    if message.text == "Добавить категорию":
        msg = bot.send_message(message.chat.id, "Введите имя категории")

        return bot.register_next_step_handler(msg, new_category)

    elif message.text in categorys:
        products(message)
    elif message.text == "Назад":
        admin_panel(message)


def new_category(message):
    if message.text != "Добавить категорию":
        data = read_json()
        new = {message.text: {}}
        data["product"].update(new)

        with open("settings", "w") as json_data:
            json.dump(data, json_data)

        msg = bot.send_message(message.chat.id, "Новая категория '{}' добавлена.".format(message.text))
        after_panel(message, "Категории")


def products(message, category_name=None):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.InlineKeyboardButton(text="Добавить изделие"),
                 types.InlineKeyboardButton(text="Назад")
                 )

    data = read_json()
    if category_name:
        category = category_name
    else:
        category = message.text

    data["current_category"]= category

    with open("settings", "w") as json_data:
        json.dump(data, json_data)

    for product in data["product"][category]:
        keyboard.add(types.InlineKeyboardButton(text=product))

    msg = bot.send_message(message.chat.id, "Редактируйте изделия в категории '{}'".format(category),
                       reply_markup=keyboard)

    return bot.register_next_step_handler(msg, after_product)


def after_product(message):
    if message.text == "Добавить изделие":
        msg = bot.send_message(message.chat.id, "Введите название изделия")
        return bot.register_next_step_handler(msg, new_product)

    elif message.text == "Назад":
        after_panel(message, "Категории")


def new_product(message):
    if message.text != "Добавить изделие":
        data = read_json()
        new = {message.text: {}}
        category = data["current_category"]
        data["product"][category].update(new)
        data["current_category"] = ""

        with open("settings", "w") as json_data:
            json.dump(data, json_data)

        bot.send_message(message.chat.id, "Новое изделие '{0}' добавленo в категорию {1}.".format(message.text,
                                                                                                  category))
        products(message, category )

