import telegram
from telegram.ext import Updater
from telegram import Update , InlineKeyboardButton, InlineKeyboardMarkup, TelegramError
from telegram import InputMediaPhoto, InputMediaVideo
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler,MessageHandler,Filters, CallbackQueryHandler, ContextTypes, JobQueue
import logging
import json
from datetime import datetime
from scraper import Buff, Market
from data.db import getSendings, updateSending
import os.path as pt
import time

def parseFromMarket(context : CallbackContext) :
    market = Market()
    buff = Buff()
    market.parse()
    buff.parse()

def sendOrder(context : CallbackContext) :
    data = getSendings()
    for i in data:
        info = json.loads(i[1])
        message = f"""{info['marketHashName']}

Профит: {info['profit']} %
Цена на Market: {info['marketPriceUsd']} $
Цена на Buff: {info['buffPriceUsd']} $

Количество на Market: {info['marketVolume']}
Количество на Buff: {info['buffVolume']}
"""
        keyboard= [
            [InlineKeyboardButton('Market', url = info['marketUrl'])],
            [InlineKeyboardButton('Buff', url = info['buffUrl'])]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=CHANNEL, text=message, reply_markup=reply_markup)
        updateSending(i[0])
        time.sleep(2)

def start(update: Update , context : CallbackContext) :
    market = Market()
    buff = Buff()
    market.parse()
    buff.parse() 

    context.bot.send_message(chat_id=update.effective_chat.id, text='Джобы запущены')
    context.job_queue.run_repeating(parseFromMarket,120, context=update.message.chat_id)
    context.job_queue.run_repeating(sendOrder,60, context=update.message.chat_id)

def stop(update: Update , context : CallbackContext ) :
    context.job_queue.stop()
    context.bot.send_message(chat_id=update.effective_chat.id, text='Джобы остановлены')

if __name__ == "__main__" :
    TOKEN = "6290678020:AAFy9CdpJhcavRMLJAJEj5_Vr6MUsoIgBBs"
    CHANNEL = '@tradersBaituk'
    
    bot = telegram.Bot(token=TOKEN)
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    stop_handler = CommandHandler('stop', stop)
    dispatcher.add_handler(stop_handler)
    
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
    updater.start_polling()

    updater.idle()