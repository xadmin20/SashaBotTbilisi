from telebot.types import Message
from loguru import logger

from tgbot.dispatcher import bot
from tgbot.services import send_error_to_admins

logger.add("logs/startbot.log", rotation="10 MB", level="DEBUG",
           format="{time} {level} {message} {file} {line} {function}")


@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_members(message: Message):
    """Приветствует новых пользователей в чате
    :param message: Объект сообщения"""
    try:
        for new_member in message.new_chat_members:
            logger.info(f"Новый пользователь: {new_member}")

            if new_member.is_bot or new_member.id == bot.get_me().id:
                continue  # Игнорируем ботов
            logger.info(message.chat.username)
            if message.chat.username == 'tsgtest':  # Проверяем, что это нужный чат по username без @
                welcome_text = f"Привет, {new_member.first_name}! Добро пожаловать в нашу группу!"
                bot.send_message(message.chat.id, welcome_text)

    except Exception as e:
        logger.error(f"Ошибка в обработчике новых пользователей: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка при обработке новых пользователей.")


@bot.message_handler(commands=['check'])
def check_membership(message):
    user_id = message.from_user.id
    chat_id = "@tsgtest"  # username @channel or chat id

    try:
        logger.info(f"Проверка подписки пользователя {user_id}")
        # Пытаемся получить информацию о членстве пользователя
        chat_member = bot.get_chat_member(chat_id, user_id)
        logger.info(f"Информация о пользователе: {chat_member}")
        # Если статус не 'left' и не 'kicked', пользователь является участником
        logger.info(f"{chat_member.status=}")
        if chat_member.status != 'left' and chat_member.status != 'kicked' or chat_member.status == 'member':
            logger.info(f"Пользователь {user_id} подписан на канал")

        else:
            bot.send_message(chat_id, "Вы не подписаны на этот канал.")
        send_error_to_admins(f"Пользователь {user_id} проверил подписку на канал.")
    except Exception as e:
        logger.exception(f"Ошибка при проверке подписки: {e}")
