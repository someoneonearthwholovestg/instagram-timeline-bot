# PapagyeInsta-Bot
Instagram Following Telegram Bot

You can follow instagram user/tag using Telegram!
****

## Requirements
* Python 3.x
* [Python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
* BeautifulSoup 4
* dotenv
* requests

## Installation
1. Clone repository first:
```git clone https://github.com/tycheyoung/PapagyeInsta-Bot.git```
2. Install prerequisites with:
```pip install -r requirements.txt```
3. Add your TOKEN(from [@Botfather](http://t.me/botfather)) and Admin ID(to make it private) to ``.envs`` file like this:
```
TELEGRAM_TOKEN='Your TOKEN from @Botfather'
GROUP_ID_1='1st Admin ID'
GROUP_ID_2='2nd Admin ID'
```

e.g.
```
TELEGRAM_TOKEN='QWERTYUIOPLKJHGFDSAZXCVBNM09:8765434567Y'
GROUP_ID_1='123456789'
GROUP_ID_2='123456789'
```

You can delete/add admin -> both ``.envs`` and ``telegram_bot.py``.

4. Run Telegram bot:
```python3 telegram_bot.py```

## Instruction
*  `/add_user [Instagram ID]` : Subscribe **`USER`**
*  `/remove_user [Instagram ID]` : Unsubscribe **`USER`**
*  `/add_tag [TAG]` : Subscribe **`TAG`**
*  `/remove_tag [TAG]` : Unsubscribe **`TAG`**
*  `/show_latest_user [Instagram ID]` : Show latest post from **`USER`**
*  `/show_latest_tag [TAG]` : Show latest post from **`TAG`**
*  `/initiate` : Flush all subscription list
*  `/list` : Show subscription list
*  `/on` : Turn push notification **ON**
*  `/off` : Turn push notification **OFF**
*  `/help` : Show help

## TODO
* Multi-user support
