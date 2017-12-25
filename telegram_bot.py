#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import url_request
import csv
import os, sys
import time
from dotenv import load_dotenv

# PreLoad dryscrape Module
import dryscrape
import webkit_server
dryscrape.start_xvfb()
server = webkit_server.Server()
server_conn = webkit_server.ServerConnection(server=server)
driver = dryscrape.driver.webkit.Driver(connection=server_conn)
sess = dryscrape.Session(driver=driver)

filename = 'subscribe.csv'
job_queue_flag = 0

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
token = os.getenv('TELEGRAM_TOKEN')


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(bot, update):
    update.message.reply_text('What you can order: \n /add, /remove, /list, /on, /off, /initiate')

def subscription_list(bot, update):
    """Echo the subscription list."""
    if(os.path.exists(filename)==0):
        update.message.reply_text('Add subscribe list first')
    else:
        update.message.reply_text("\n".join(url_request.print_subscribe_list()))

def initiate(bot, update):
    """Flush all subscription list."""
    url_request.initiate_list()
    update.message.reply_text('Terminated all subscription list!')

def add_subscription(bot, update, args):
    """Add Instagram ID to subscription list."""
    chat_id = update.message.chat_id
    try:
        results = url_request.add_subscribe(args[0])
        if (results == -2):
          update.message.reply_text('Successfully added to subscription list!')
        elif (results == -3):
          update.message.reply_text('Already exists in subscription list!')
        elif (results == -4):
          update.message.reply_text("Page doesn't exist or private account")
          
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <Instagram ID>')

def unsubscribe(bot, update, args):
    """Add Instagram ID to subscription list."""
    chat_id = update.message.chat_id
    try:
        results = url_request.unsubscribe(args[0])
        if (results == -3):
          update.message.reply_text('There is nothing to unsubscribe')
        elif (results == -2):
          update.message.reply_text('Successfully removed from subscription list!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /remove <Instagram ID>')

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def callback_feedupdater(bot, job):
    with open(filename, 'rt') as infile, open('outfile.csv', 'a') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        try:
            for row in reader:
                profile = url_request.profile_address(row[0])
                # print(profile)
                url_temp = url_request.find_latest(profile)
                if(row[1]!=url_temp):
                    row[1] = url_temp
                    bot.send_message(chat_id=job.context, text=row[1])
                try:
                    writer.writerow(row)
                except IndexError:
                    bot.send_message(chat_id=job.context, text=row[0]+'changed to private account or not existing')
#                time.sleep(20)
            os.remove(filename)
            os.rename("outfile.csv", filename)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
            bot.send_message(chat_id=job.context, text='CSV File Error!')

def callback_timer(bot, update, job_queue):
    if(job_queue_flag==1):
        job_queue.schedule_removal()
    elif(job_queue_flag==0):
        bot.send_message(chat_id=update.message.chat_id,
                         text='Notification ON!')
        job_queue.run_repeating(callback_feedupdater, interval=60, context=update.message.chat_id)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='FLAG ERROR')

def notify_off(bot, update, job_queue):
    bot.send_message(chat_id=update.message.chat_id, text='Notification OFF!')
    job_queue_flag = 1

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token) # YOUR TOKEN HERE

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Cron_updater
    feed_handler = CommandHandler("on", callback_timer, pass_job_queue=True)
    dp.add_handler(feed_handler)
    dp.add_handler(CommandHandler("off", notify_off, pass_job_queue=True))
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("hello", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("initiate", initiate))
    dp.add_handler(CommandHandler("list", subscription_list))
    dp.add_handler(CommandHandler("add", add_subscription, pass_args=True))
    dp.add_handler(CommandHandler("remove", unsubscribe, pass_args=True))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    logger.info('Started!')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
