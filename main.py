#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import TelegramError
import telegram
from functools import wraps
import urllib.request
import logging
import re
import subprocess
import configparser
import os

config = configparser.ConfigParser()

config.read('settings.ini')

INPUT_FILE  = config['video.settings']['input']
OUTPUT_FILE = config['video.settings']['output']
FFMPEG_BIN  = config['video.settings']['bin']

CMD = [FFMPEG_BIN, 
       '-i', INPUT_FILE,
       '-c:v', 'libx264',
       '-b:v', config['ffmpeg.settings']['bv'], 
       '-preset','veryslow',
       '-c:a', 'aac', 
       '-b:a', config['ffmpeg.settings']['ba'],
       '-loglevel', 'panic', '-y',
       OUTPUT_FILE]

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

<<<<<<< HEAD
=======
# admin privileges decorator
def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        try:
            user_id = update.message.from_user.id
        except (NameError, AttributeError):
            try:
                user_id = update.inline_query.from_user.id
            except (NameError, AttributeError):
                try:
                    user_id = update.chosen_inline_result.from_user.id
                except (NameError, AttributeError):
                    try:
                        user_id = update.callback_query.from_user.id
                    except (NameError, AttributeError):
                        print("No user_id available in update.")
                        return
        if user_id not in ADMIN:
            print("Unauthorized access denied for {}.".format(chat_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

>>>>>>> ad0b40953b4b90e6e3640a252f218fef497e8053
# delete files after converting
def delete_files():
    os.remove(INPUT_FILE)
    os.remove(OUTPUT_FILE)   

# convert webm 2 mp4 handler
def convert_webm(bot, update):
    try:
        url = re.search('(?P<url>https?:\/\/[^\s]+.webm)', update.message.text).group('url')
        if url:
            logger.info("url fetched: %s", url)
        with urllib.request.urlopen(url) as resp, open(INPUT_FILE,'wb') as file:
            data = resp.read();
            file.write(data)
            print(os.stat(INPUT_FILE).st_size)
            if file:
                logger.info("fetched filesize: %0.0iK", os.stat(INPUT_FILE).st_size/1024)
            subprocess.run(CMD)
            bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.UPLOAD_VIDEO)
            bot.send_video(chat_id=update.message.chat_id, video=open(OUTPUT_FILE, 'rb'), quote = True)
            logger.info("converted filesize: %0.0iK", os.stat(OUTPUT_FILE).st_size/1024)     
        delete_files()
    # todo: fix this with bot API filters
    except AttributeError:
        None
    except TelegramError as e:
        logger.error(e)
    
updater = Updater(token = config['default']['token'])

dp = updater.dispatcher
    
dp.add_handler(MessageHandler(Filters.text, convert_webm))

if updater.start_polling():
    logger.info("bot started!")
    updater.idle()

if __name__ == '__main__':
    main()
