from telethon import TelegramClient
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
django.setup()

session = 'client'
api_id = 23180312
api_hash = "e811f4c1e6d41bd3c28e782b0e568cf5"

client = TelegramClient(session, api_id, api_hash).start()
