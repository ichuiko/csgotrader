import telegram
from telegram.ext import Updater
from telegram import Update , InlineKeyboardButton, InlineKeyboardMarkup, TelegramError
from telegram import InputMediaPhoto, InputMediaVideo
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler,MessageHandler,Filters, CallbackQueryHandler, ContextTypes, JobQueue
import logging
from datetime import datetime
from scraper import parseData

def parseFromMarket(update: Update , context : CallbackContext) :
    parseData(1)
    context.bot.send_message(chat_id=3313923891, text='')

def start(update: Update , context : CallbackContext) :
    context.bot.send_message(chat_id=update.effective_chat.id, text='Rabotaem')
    context.job_queue.run_repeating(parseFromMarket,60, context=update.message.chat_id)

if __name__ == "__main__" :
    TOKEN = "6290678020:AAFy9CdpJhcavRMLJAJEj5_Vr6MUsoIgBBs"
    
    bot = telegram.Bot(token=TOKEN)
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
    updater.start_polling()

    updater.idle()