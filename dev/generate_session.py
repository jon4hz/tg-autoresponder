from telethon.sync import TelegramClient
from data.config import config

API_ID = config['telegram']['api_id']
API_HASH = config['telegram']['api_hash']
PHONE = config['telegram']['phone']

with TelegramClient(PHONE, API_ID, API_HASH) as client:
    string = client.session.save()
