import os
import sys
import signal
import time
import sqlite3
from django.core.management.base import BaseCommand
from logger_setup import logger
from telethon import TelegramClient
from tgbot.commands import handler
from tgbot.dispatcher import client


class Command(BaseCommand):
    help = "Запускает бота на платформе Telegram"

    def handle(self, *args, **options):

        def shutdown_handler(signum, frame):
            logger.info("Shutting down bot...")
            sys.exit(0)

        signal.signal(signal.SIGINT, shutdown_handler)
        signal.signal(signal.SIGTERM, shutdown_handler)

        # session = os.environ.get('TG_SESSION', 'printer')
        # api_id = 20095274
        # api_hash = "c70536d9ef963383dab8514e7106c776"
        # proxy = None

        while True:
            try:
                logger.info("Bot started")

                retries = 5
                while retries:
                    try:

                        client.add_event_handler(handler)
                        client.run_until_disconnected()
                    except sqlite3.OperationalError as e:
                        logger.error(f"SQLite error: {str(e)}")
                        retries -= 1
                        if retries == 0:
                            raise
                        time.sleep(2)
                    else:
                        break
            except Exception as e:
                logger.error(f"Error polling: {str(e)}")
                logger.exception("Bot polling failed, restarting...")
                time.sleep(5)
