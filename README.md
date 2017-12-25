# PapagyeInsta-Bot
Private Instagram Following Telegram Bot

You can follow someone without showing that you are following someone to your friends!
****

## Requirements
* Python 3.x
* Python-telegram-bot <https://github.com/python-telegram-bot/python-telegram-bot>_
* BeautifulSoup 4
* dryscrape
* dotenv


## Installation
1. ```git clone https://github.com/tycheyoung/PapagyeInsta-Bot.git```

2. ```$vim .env```

Add your TOKEN from @Botfather to ``.env`` file like this:
> TELEGRAM_TOKEN='Your TOKEN from @Botfather'

3. ```$python3 telegram_bot.py```

## Instruction
*  `/add [Instagram ID]` : Subscribe **`USER`**
*  `/remove [Instagram ID]` : Unsubscribe **`USER`**
*  `/initiate` : Flush all subscription list
*  `/list` : Show subscription list
*  `/on` : Turn push notification **ON**
*  `/off` : Turn push notification **OFF**
*  `/help` : Show help

## TODO
* Multi-user support
