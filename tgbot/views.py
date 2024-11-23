from django.shortcuts import render
import json
import logging
import os
import time
import uuid
from datetime import datetime

import redis
from django.core.exceptions import ValidationError
from django.db import InterfaceError, connection, OperationalError, transaction
from loguru import logger as loguru_logger
from django.utils.timezone import make_aware
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from core.models import TelegramUser, Wallet, GreetingMessage
from core.services import tail, create_log_file
from core.statistics_web_socket import ActiveUsers
from tgbot.dispatcher import bot, TelegramLoggingHandler
from tgbot.services import get_daily_user_counts, calculate_percentage_change, language_keyboard, continue_registration, \
    process_language_selection

# Настройка основного логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Устанавливаем уровень логгирования для логгера
loguru_logger.add("logs/startbot.log", rotation="10 MB", level="DEBUG", format="{time} {level} {message} {file} {line} {function}")
# Настройка файлового обработчика
file_handler = logging.FileHandler("logs/startbot.log")
file_handler.setLevel(logging.INFO)  # Устанавливаем уровень логгирования для файлового обработчика
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Настройка обработчика для Telegram
telegram_handler = TelegramLoggingHandler(chat_id=91124946)
telegram_handler.setLevel(logging.ERROR)  # Уровень логгирования для этого обработчика

# Добавление обработчиков к логгеру
logger.addHandler(file_handler)
logger.addHandler(telegram_handler)

# Настройка клиента Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Create your views here.
@bot.message_handler(commands=['redis'])
def send_redis_data(message):
    try:
        print("Fetching data from Redis...")
        data = fetch_redis_data()
        save_data_to_file(data)
        with open('redis_data.json', 'rb') as data_file:
            bot.send_document(message.chat.id, data_file)
    except Exception as e:
        print(e)
        logger.error(f"An error occurred: {e}")
        bot.reply_to(message, f"Error occurred: {str(e)}")

def fetch_redis_data():
    """Fetch all data from Redis and return as a dictionary."""
    keys = redis_client.keys('*')  # Получение всех ключей
    data = {}
    for key in keys:
        value = redis_client.get(key)
        # Проверка и декодирование значения, если это необходимо
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        # Проверка и декодирование ключа, если это необходимо
        if isinstance(key, bytes):
            key = key.decode('utf-8')
        data[key] = value
    return data

def save_data_to_file(data):
    """Save the given data to a JSON file."""
    with open('redis_data.json', 'w') as file:
        json.dump(data, file, indent=4)