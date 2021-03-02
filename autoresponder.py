#!/usr/bin/env python3
#
# Author: jon4hz
# Date: 02.03.20201
# Desc: Telegram Userbot for autoresponding to message
#
#######################################################################################################################
try:
    import asyncio, json, os, sys, aiosqlite
    from datetime import datetime
    from telethon import TelegramClient, events
    from data.message import text as MESSAGE
    from data.config import config
except ImportError as e:
    print(f'Error could not import modules - {e}')

# Reading configs
try:
    # telegram client credentials
    API_ID = config['telegram']['api_id']
    API_HASH = config['telegram']['api_hash']
    PHONE = config['telegram']['phone']
    # DB
    DB_FILE = config['database']['file']
    # Autoresponder
    EXCLUDED_USERS = config['autoresponder']['excluded_users']
    TIMEOUT = config['autoresponder']['timeout']
except Exception as e:
    print(f'{datetime.utcnow()} - Error: Could not read variables from config file.\n - Missing Key: {e}')
    sys.exit(1)

# check if session files exist
if not os.path.isfile(f'data/{PHONE}.session'):
    print("Session files not found! Please execute 'sudo docker-compose run autoresponder' to generate them!")
    exit(1)

# create client
try:
    client = TelegramClient(f'data/{PHONE}', API_ID, API_HASH)
except Exception as e:
    print(f'{datetime.utcnow()} - Error: Could not create client. - {e}')
    sys.exit(1)


async def setup_inital_database(database) -> None:
    try:
        async with aiosqlite.connect(database) as db:
            await db.execute('DROP TABLE IF EXISTS data;')
            await db.execute('''
                CREATE TABLE data(id INTEGER PRIMARY KEY, last_contacted INTEGER);
            ''')
            await db.commit()
    except Exception as e:
        print(f'{datetime.utcnow()} - Error: could not create database. Aborting now! - {e}')
        sys.exit(1)


async def get_data_from_database(database, tg_id) -> int:
    try:
        async with aiosqlite.connect(DB_FILE) as db:
            async with db.execute(f'''
                SELECT * FROM data where id={tg_id};
            ''') as cur:
                async for row in cur:
                    return row[1]
    except Exception as e:
        print(f'{datetime.utcnow()} - Error: {e}')
        if "no such table" in str(e):
            await setup_inital_database(DB_FILE)

# listener
@client.on(events.NewMessage())
async def handler(event) -> None:
    if (event.is_private and 
        not (await event.get_sender()).bot and 
        not event.message.out and
        event.sender_id not in EXCLUDED_USERS):
        
        # check if user in database
        last_contacted = await get_data_from_database(DB_FILE, event.sender_id)
   
        if last_contacted:
            if ((datetime.utcnow().timestamp()-last_contacted) /60) > int(TIMEOUT):
                
                # trigger autoresponder
                await client.send_message(event.sender_id, reply_to=event.message.id, message=MESSAGE, link_preview=False)

            # update last_contacted time
            try:
                async with aiosqlite.connect(DB_FILE) as db:
                    await db.execute(f'''
                        UPDATE data
                        SET last_contacted={datetime.utcnow().timestamp()}
                        WHERE id={event.sender_id};
                    ''')
                    await db.commit()
            except Exception as e:
                print(f'{datetime.utcnow()} - Error: {e}')
                if "no such table" in str(e):
                    await setup_inital_database(DB_FILE)
        else:
            # insert user to database
            try:
                async with aiosqlite.connect(DB_FILE) as db:
                    await db.execute(f'''
                        INSERT INTO data(id, last_contacted) VALUES
                        ({event.sender_id},{datetime.utcnow().timestamp()})
                    ''')
                    await db.commit()
            except Exception as e:
                print(f'{datetime.utcnow()} - Error: {e}')
                if "no such table" in str(e):
                    await setup_inital_database(DB_FILE)
            
            # trigger autoresponder
            await client.send_message(event.sender_id, reply_to=event.message.id, message=MESSAGE, link_preview=False)


if __name__ == "__main__":

    # check if database file exists
    if not os.path.isfile(DB_FILE):
        asyncio.run(setup_inital_database(DB_FILE))

    # start the client
    client.start()
    print("Client started...")
    client.run_until_disconnected()
    print("Client closed...")