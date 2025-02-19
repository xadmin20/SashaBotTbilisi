from telethon import events
from telethon.tl.types import UpdateNewMessage, UpdateShortChatMessage, Message, UpdateUserStatus, \
    UpdateReadHistoryInbox

from logger_setup import logger
from tgbot.dispatcher import client
from tgbot.services import forward_message, process_message


def start_command_in_private(event):
    return event.is_private and event.raw_text.strip() == '/start'

@client.on(events.NewMessage(func=start_command_in_private))
async def handler(event):
    await event.reply('Привет! Команда /start доступна только в личных сообщениях.')


@client.on(events.NewMessage)
async def handler(event):
    try:
        if isinstance(event, UpdateUserStatus) or isinstance(event, UpdateReadHistoryInbox) or isinstance(event, UpdateShortChatMessage):
            return

        if isinstance(event, events.NewMessage.Event):
            response = await forward_message(client, event)
            logger.info(f"Сообщение: {response=}")
            users = await process_message(response['message'])
            logger.info(f"Пользователи: {users=}")

            msg = f"""
Сообщение: {response['message']}
Чат: {response['chat_name']}
Ссылка: {response['message_link']}
"""
            for user in users:
                await client.send_message(user, msg)
            return

        logger.info(f"Получено новое событие: {event}")
        logger.info(f"Type: {type(event)}")

    except Exception as e:
        logger.exception(f"Ошибка обработки события: {e}")


@client.on(events.Raw)
async def raw_handler(event):
    try:
        # Игнорируем низкоуровневые события, которые уже обработаны
        if isinstance(event, UpdateShortChatMessage):
            logger.info("Пропускаем событие UpdateShortChatMessage, оно уже обработано.")
            return
        elif isinstance(event, UpdateUserStatus):
            # Игнорируем обновления статуса пользователя
            return

        # Логируем все другие необработанные события
        logger.info(f"Необработанное событие: {type(event)}")
    except Exception as e:
        logger.exception(f"Ошибка обработки необработанного события: {e}")