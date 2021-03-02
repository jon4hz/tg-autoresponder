# tg-autoresponder

## About
This userbot is an autoresponder that responds with a predefined message if no message has been received for a certain time. The timeout time gets calculated for every user.  
The timeout is set for each user individually. The userbot only responds to messages from persons. Messages from groups or bots will be ignored.

## Prerequisites
To use the autoresponder you'll need to create a Telegram Application. Follow this [tutorial](https://core.telegram.org/api/obtaining_api_id) if you are unfamiliar with that.

## Setup
### Build the image
To build the image use `sudo docker-compose build`

### Environment variables
Set all required variables in the file `env_autoresponder`.

| Var | Function | Default |
| --- | --- | --- |
| TELEGRAM_API_ID | Telegarm API ID | - |
| TELEGRAM_API_HASH | Telegarm API HASH | - |
| TELEGRAM_PHONE | Your phone number | - |
| DATABASE_FILE | Location of the database file | data/database.db |
| AUTORESPONDER_TIMEOUT | Timeout in minutes | 60 |

### Inital setup
Since telethon generates a session file the first startup, the container must be started initially  with `sudo docker-compose run autoresponder`.
After that it stores the session file and the container can be started in the background by executing `sudo docker-compose up -d`

## Customization
### Autoresponder Message
The message which will be sent is located in `./data/message.py`. After editing the message, restart the container with `sudo docker-compose restart`.

### Exclude users
There is an option to exclude users from receiving the automated message. Add a users telegram id in the `excluded_users` array in the file `./data/config.py`.