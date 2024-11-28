

from telethon.tl.types import PeerChannel, PeerChat, Message
from tgbot.models import Keyword
from logger_setup import logger

from asgiref.sync import sync_to_async
import pymorphy2


# Инициализация анализатора
morph = pymorphy2.MorphAnalyzer()

def generate_word_forms(word: str) -> set:
    """
    Генерация различных форм слова.
    :param word: Исходное слово.
    :return: Набор словоформ.
    """
    try:
        parsed_word = morph.parse(word)[0]
        word_forms = {form.word for form in parsed_word.lexeme}  # Все формы слова
        return word_forms
    except Exception as e:
        logger.exception(f"Ошибка генерации словоформ для слова {word}: {e}")
        return {word}  # Если ошибка, возвращаем само слово

async def process_message(message_text: str) -> list:
    """
    Обработка текста сообщения и возврат списка телеграм-айди пользователей, которые подходят.
    """
    try:
        message_text_lower = message_text.lower()
        logger.info(f"Message text: {message_text_lower}")
        matched_users = set()

        # Асинхронно получаем все ключевые слова из базы данных
        keywords = await sync_to_async(list)(Keyword.objects.select_related('specialty').all())
        logger.info(f"Keywords: {keywords}")

        for keyword in keywords:
            # Генерация всех словоформ для ключевого слова
            logger.debug(f"Обрабатываем слово: {keyword.word}")
            word_forms = generate_word_forms(keyword.word.lower())
            logger.info(f"Словоформы для '{keyword.word}': {word_forms}")

            # Проверка, содержится ли хотя бы одна форма слова в тексте сообщения
            if any(form in message_text_lower for form in word_forms):
                # Асинхронно получаем пользователей по специальности
                users_with_specialty = await sync_to_async(list)(keyword.specialty.users.all())
                matched_users.update(users_with_specialty)

        logger.info(f"Matched users: {matched_users}")
        return [user.telegram_id for user in matched_users]
    except Exception as e:
        logger.exception(f"Error processing message: {e}")
        return []
# Функция для формирования ссылки и пересылки сообщения


async def forward_message(client, event) -> dict or None:
    try:
        # Проверяем, содержит ли событие сообщение
        if not hasattr(event, 'message'):
            logger.exception("Событие не содержит атрибут 'message'.")
            return
        if not isinstance(event.message, Message):
            logger.exception(f"Тип атрибута 'message' некорректен: {type(event.message)}")
            return

        original_message = event.message.message  # Текст сообщения
        logger.info(f"{original_message=}")

        # Извлекаем информацию о чате
        peer = event.message.peer_id  # Peer объекта

        # Проверяем тип чата
        if isinstance(peer, PeerChannel):  # Если сообщение из канала
            chat = await client.get_entity(peer.channel_id)
            chat_name = chat.title or "Unknown Channel"
            chat_username = chat.username
            message_id = event.message.id

            # Формируем ссылку, если это публичный канал
            if chat_username:
                message_link = f"https://t.me/{chat_username}/{message_id}"
            else:
                message_link = "Ссылка недоступна (канал приватный)"
        elif isinstance(peer, PeerChat):  # Если сообщение из группы
            chat = await client.get_entity(peer.chat_id)
            chat_name = chat.title or "Unknown Group"
            message_link = "Ссылки на сообщения недоступны для групп."
        else:
            logger.error("Неизвестный тип чата.")
            return

        result = {
            "chat_name": chat_name,
            "message": original_message,
            "message_link": message_link
        }

        logger.info(f"{result=}")
        return result
    except Exception as e:
        logger.exception(f"Ошибка пересылки сообщения: {e}")
