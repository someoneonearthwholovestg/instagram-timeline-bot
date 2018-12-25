# PapagyeInsta-Bot
Private Instagram Following Telegram Bot

You can follow someone without showing that you are following someone to your friends!
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
3. Add your TOKEN(from [@Botfather](http://t.me/botfather)) to ``.envs`` file like this:
> TELEGRAM_TOKEN='Your TOKEN from @Botfather'

e.g.
> TELEGRAM_TOKEN='QWERTYUIOPLKJHGFDSAZXCVBNM09:8765434567Y'

4. Run Telegram bot
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
