#  encoding: utf-8
# based on https://habr.com/post/316666/ by @saluev

import configparser
import random

import base58
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

from Intendant.static import get, MyLogger

config = configparser.ConfigParser()
config.read('config.ini', 'utf-8')

BOT_TOKEN = config.get('bot', 'BOT_TOKEN')

LOGGING_SERVER = config.get('logging', 'SERVER')
LOGGING_PORT = int(config.get('logging', 'PORT'))

START_TEXT = config.get('text', 'START_TEXT')
HELP_TEXT = config.get('text', 'HELP_TEXT')
WRONG_VALUE_TEXT = config.get('text', 'WRONG_VALUE_TEXT')
ERROR_TEXT = config.get('text', 'ERROR_TEXT')
TOO_HIGH_TEXT = config.get('text', 'TOO_HIGH_TEXT')
SUCCESS_TEXT = config.get('text', 'SUCCESS_TEXT')
COMMANDS_TEXT = config.get('text', 'COMMANDS_TEXT')

MIN_AMOUNT = int(config.get('settings', 'MIN_AMOUNT'))
MAX_AMOUNT = int(config.get('settings', 'MAX_AMOUNT'))
SERVER = config.get('settings', 'SERVER')
ADD_DONATION = config.get('settings', 'ADD_DONATION')

DESCRIPTIONS = config.get('samples', 'DESCRIPTIONS').split(',')
ACCOUNTS = config.get('samples', 'ACCOUNTS').split(',')

logger = MyLogger(LOGGING_SERVER, LOGGING_PORT)


def start(bot, update):
    # подробнее об объекте update: https://core.telegram.org/bots/api#update
    bot.sendMessage(chat_id=update.message.chat_id, text=START_TEXT + ' ' + COMMANDS_TEXT)


def help(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=HELP_TEXT + ' ' + COMMANDS_TEXT)


def success(bot, update, amount):
    donation_id = add_donation(amount)
    bot.sendMessage(chat_id=update.message.chat_id, text=SUCCESS_TEXT)
    bytecode = base58.b58encode_check(bytes(donation_id, 'utf-8'))
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=bytecode.decode('utf-8'))


def error(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=ERROR_TEXT)


def wrong_value(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=WRONG_VALUE_TEXT)


def too_high(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=TOO_HIGH_TEXT)


def handle_message(bot, update):
    message = update.message.text
    try:
        message = int(message)
        if MIN_AMOUNT <= message:
            if message > MAX_AMOUNT:
                too_high(bot, update)
            else:
                success(bot, update, message)
                return
    except ValueError as ve:
        logger.debug(message, ve)
        wrong_value(bot, update)
    except Exception as exc:
        logger.error(message, exc)
        error(bot, update)


def add_donation(amount):
    url = SERVER + '/' + ADD_DONATION
    params = {'amount': amount, 'description': random.choice(DESCRIPTIONS), 'accountNumber': random.choice(ACCOUNTS)}
    answer = get(url, params)
    logger.info(f'add_donation answer = {answer}')
    return answer['key']


updater = Updater(token=BOT_TOKEN)

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)

message_handler = MessageHandler(Filters.text, handle_message)

updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(help_handler)
updater.dispatcher.add_handler(message_handler)
updater.start_polling()
