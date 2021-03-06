#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import url_request
import csv
import os
import sys
import time
from threading import Thread
from dotenv import load_dotenv
from functools import wraps
import portalocker

filename = 'subscribe_user.csv'
filename_2 = 'subscribe_tag.csv'
job_queue_flag = 0

dotenv_path = os.path.join(os.path.dirname(__file__), '.envs')
load_dotenv(dotenv_path)
token = os.getenv('TELEGRAM_TOKEN')
group_id_1 = int(os.getenv('GROUP_ID_1'))
group_id_2 = int(os.getenv('GROUP_ID_2'))  # You can add up Admin ID 

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
          level=logging.INFO)

logger = logging.getLogger(__name__)

# Make Bot Private
LIST_OF_ADMINS = [group_id_1, group_id_2]

def restricted(func):
  @wraps(func)
  def wrapped(bot, update, *args, **kwargs):
    user_id = update.effective_user.id
    if user_id not in LIST_OF_ADMINS:
      print("Unauthorized access denied for {}.".format(user_id))
      return
    return func(bot, update, *args, **kwargs)
  return wrapped
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
  """Send a message when the command /start is issued."""
  update.message.reply_text('Hi!')

def help(bot, update):
  update.message.reply_text('What you can order: \n /r(restart), /add_user, /remove_user, /add_tag, /remove_tag, /show_latest_user, /show_latest_tag, /list, /on, /off, /initiate, /reload_posts')

@restricted
def subscription_list(bot, update):
  """Echo the subscription list."""
  if(os.path.exists(filename)==0 and os.path.exists(filename_2)==0):
    update.message.reply_text('Add subscribe list first')
  else:
    if(os.path.exists(filename)!=0):
      update.message.reply_text('User:\n'+"\n".join(url_request.print_subscribe_list(filename)), quote=False)
    if(os.path.exists(filename_2)!=0):
      update.message.reply_text('Tag:\n'+"\n".join(url_request.print_subscribe_list(filename_2)), quote=False)

@restricted
def reload_posts(bot, update):
  """Reload latest post in subscription"""
  try:
    with open(filename, 'rt', encoding='utf-8') as f:
      reader = csv.reader(f)
      for row in reader:
        if (row[1] != 'NULL'):
          update.message.reply_text('Latest post from '+row[0]+':\n'+row[1], quote=False)
        else:
          update.message.reply_text(row[0]+': changed to private account or not existing', quote=False)
  except (OSError, IOError):
    print('CSV File Error! (reload_post)')

@restricted
def initiate(bot, update):
  """Flush all subscription list."""
  url_request.initiate_list(filename)
  url_request.initiate_list(filename_2)
  url_request.initiate_list("outfile.csv")
  url_request.initiate_list("outfile_2.csv")
  update.message.reply_text('Terminated all subscription list!')

@restricted
def add_subscription_user(bot, update, args):
  """Add Instagram ID to subscription list."""
  chat_id = update.message.chat_id
  try:
    results = url_request.add_subscribe(args[0], filename, 0)
    if (results == -2):
      update.message.reply_text('Successfully added to subscription list!')
    elif (results == -3):
      update.message.reply_text('Already exists in subscription list!')
    elif (results == -4):
      update.message.reply_text("Page doesn't exist or private account")
      
  except (IndexError, ValueError):
    update.message.reply_text('Usage: /add_user <Instagram ID>')

@restricted
def unsubscribe_user(bot, update, args):
  """Remove Instagram ID to subscription list."""
  chat_id = update.message.chat_id
  try:
    results = url_request.unsubscribe(args[0], filename)
    if (results == -3):
      update.message.reply_text('There is nothing to unsubscribe')
    elif (results == -2):
      update.message.reply_text('Successfully removed from subscription list!')

  except (IndexError, ValueError):
    update.message.reply_text('Usage: /remove_user <Instagram ID>')

@restricted
def add_subscription_tag(bot, update, args):
  """Add Instagram TAG to subscription list."""
  chat_id = update.message.chat_id
  try:
    results = url_request.add_subscribe(args[0], filename_2, 1)
    if (results == -2):
      update.message.reply_text('Successfully added to subscription list!')
    elif (results == -3):
      update.message.reply_text('Already exists in subscription list!')
    elif (results == -4):
      update.message.reply_text("Page doesn't exist")
      
  except (IndexError, ValueError):
    update.message.reply_text('Usage: /add_tag <TAG>')

@restricted
def unsubscribe_tag(bot, update, args):
  """Remove Instagram TAG to subscription list."""
  chat_id = update.message.chat_id
  try:
    results = url_request.unsubscribe(args[0], filename_2)
    if (results == -3):
      update.message.reply_text('There is nothing to unsubscribe')
    elif (results == -2):
      update.message.reply_text('Successfully removed from subscription list!')

  except (IndexError, ValueError):
    update.message.reply_text('Usage: /remove_tag <TAG>')

def show_latest_user(bot, update, args):
  """Show latest update of USER."""
  chat_id = update.message.chat_id
  try:
    results = url_request.find_latest(url_request.profile_address(args[0]), 0)
    if (results == 'NULL'):
      update.message.reply_text("Error: Page doesn't exist/private account/No post")
    else:
      update.message.reply_text(results)

  except (IndexError, ValueError):
    update.message.reply_text('Usage: /show_latest_user <Instagram ID>')
 
def show_latest_tag(bot, update, args):
  """Show latest update of TAG."""
  chat_id = update.message.chat_id
  try:
    results = url_request.find_latest(url_request.tag_address(args[0]), 1)
    if (results == 'NULL'):
      update.message.reply_text("Result does not exist")
    else:
      update.message.reply_text(results)

  except (IndexError, ValueError):
    update.message.reply_text('Usage: /show_latest_tag <TAG>')

def error(bot, update, error):
  """Log Errors caused by Updates."""
  logger.warning('Update "%s" caused error "%s"', update, error)

def callback_feedupdater(bot, job):
  # USER UPDATE
  try:
    with open(filename, 'rt', encoding='utf-8') as infile, open('outfile.csv', 'w', encoding='utf-8', newline='') as outfile:
      portalocker.lock(infile, portalocker.LOCK_EX)
      reader = csv.reader(infile)
      writer = csv.writer(outfile)
      for row in reader:
        profile = url_request.profile_address(row[0])
        url_temp = url_request.find_latest(profile, 0)
        if(row[1]!=url_temp):
          row[1] = url_temp
          if (row[1] != 'NULL'):
            bot.send_message(chat_id=job.context, text='Update from '+row[0]+':\n'+row[1])
          else:
            bot.send_message(chat_id=job.context, text=row[0]+': changed to private account or not existing')
        writer.writerow(row)
    os.replace("outfile.csv", filename)
  except (OSError, IOError):
    print('CSV File Error! (update_user)')
  # TAG UPDATE
  try:
    with open(filename_2, 'rt', encoding='utf-8') as infile, open('outfile_2.csv', 'w', encoding='utf-8', newline='') as outfile:
      portalocker.lock(infile, portalocker.LOCK_EX)
      reader = csv.reader(infile)
      writer = csv.writer(outfile)
      for row in reader:
        profile = url_request.tag_address(row[0])
        url_temp = url_request.find_latest(profile, 1)
        if(row[1]!=url_temp):
          row[1] = url_temp
          if (row[1] != 'NULL'):
            bot.send_message(chat_id=job.context, text='Update from '+row[0]+':\n'+row[1])
          else:
            bot.send_message(chat_id=job.context, text=row[0]+': does not exist')
        writer.writerow(row)
    os.replace("outfile_2.csv", filename_2)
  except (OSError, IOError):
    print('CSV File Error! (update_tag)')

@restricted
def callback_timer(bot, update, job_queue):
  if(job_queue_flag==1):
    job_queue.schedule_removal()
  elif(job_queue_flag==0):
    bot.send_message(chat_id=update.message.chat_id,
             text='Notification ON!')
    job_queue.run_repeating(callback_feedupdater, interval=1800, context=update.message.chat_id)
  else:
    bot.send_message(chat_id=update.message.chat_id, text='FLAG ERROR')

@restricted
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
  dp.add_handler(CommandHandler("on", callback_timer, pass_job_queue=True))
  dp.add_handler(CommandHandler("off", notify_off, pass_job_queue=True))
  # on different commands - answer in Telegram
  dp.add_handler(CommandHandler("hello", start))
  dp.add_handler(CommandHandler("help", help))
  dp.add_handler(CommandHandler("initiate", initiate))
  dp.add_handler(CommandHandler("list", subscription_list))
  dp.add_handler(CommandHandler("reload_posts", reload_posts))
  dp.add_handler(CommandHandler("add_user", add_subscription_user, pass_args=True))
  dp.add_handler(CommandHandler("remove_user", unsubscribe_user, pass_args=True))
  dp.add_handler(CommandHandler("add_tag", add_subscription_tag, pass_args=True))
  dp.add_handler(CommandHandler("remove_tag", unsubscribe_tag, pass_args=True))
  dp.add_handler(CommandHandler("show_latest_user", show_latest_user, pass_args=True))
  dp.add_handler(CommandHandler("show_latest_tag", show_latest_tag, pass_args=True))

  # on noncommand i.e message - echo the message on Telegram
  def stop_and_restart():
    """Gracefully stop the Updater and replace the current process with a new one"""
    updater.stop()
    os.execl(sys.executable, sys.executable, *sys.argv)

  @restricted
  def restart(bot, update):
    update.message.reply_text('Bot is restarting...')
    Thread(target=stop_and_restart).start()

  dp.add_handler(CommandHandler('r', restart))

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
