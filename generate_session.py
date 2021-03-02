#!/usr/bin/env python3
#
# Author: jon4hz
# Date: 02.03.20201
# Desc: Generate Telethon Session files
#
#######################################################################################################################
try:
    from telethon.sync import TelegramClient
    from data.config import config
except ImportError as e:
    print(f'Error could not import modules - {e}')

try:
    API_ID = config['telegram']['api_id']
    API_HASH = config['telegram']['api_hash']
    PHONE = config['telegram']['phone']
except Exception as e:
    print(f'{datetime.utcnow()} - Error: Could not read variables from config file.\n - Missing Key: {e}')
    sys.exit(1)

try:
    print("Generating session file...")
    with TelegramClient(f'data/{PHONE}', API_ID, API_HASH) as client:
        string = client.session.save()
        exit(0)
except Exception as e:
    print(f'Error - {e}')
    exit(1)
