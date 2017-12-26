from flask import Blueprint
from flask import request

from telebot import types

import telebot
import config


user = Blueprint("user", __name__)

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    make_order = types.InlineKeyboardButton(text="Хочу заказать")
    keyboard.add(make_order)

    if message.from_user.id in [388001140, 191885567]:
        from admin_board import admin_panel

        keyboard.add(types.InlineKeyboardButton(text="Настройки"))
        msg = bot.send_message(message.chat.id,
                           "Панель администратора",
                           reply_markup=keyboard)

        return bot.register_next_step_handler(msg, admin_panel)

    msg = bot.reply_to(message,
                     "Привет, {}!".format(message.from_user.first_name),
                     reply_markup=keyboard)
    return bot.register_next_step_handler(msg, kind)


def kind(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    make_order = types.InlineKeyboardButton(text="Хочу сумку")
    make_order2 = types.InlineKeyboardButton(text="Хочу ремень")
    make_order3 = types.InlineKeyboardButton(text="Хочу кошелек")
    keyboard.add(make_order, make_order2, make_order3)
    bot.send_message(message.chat.id,
                     "Валяй, {}!".format(message.from_user.first_name),
                     reply_markup=keyboard)


@user.route('/{}'.format(config.TOKEN), methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@user.route('/', methods=['POST'])
def webhook1():
    bot.remove_webhook()
    bot.set_webhook(url="{0}/{1}".format(config.HOST, config.TOKEN))
    return "!", 200

