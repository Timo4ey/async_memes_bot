# pylint: disable=no-name-in-module
import logging
from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup,InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, CallbackQueryHandler, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler

from config import tg_access_token
from memes_sender import send_memes_runner

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the bot"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )
    keyboard = [
        [
            InlineKeyboardButton('resent_memes', callback_data = '1'),
            InlineKeyboardButton('more_memes', callback_data = '0')   


        ],
        [InlineKeyboardButton('Quit', callback_data = 'cancel')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose:', reply_markup=reply_markup)


async def button(update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""

    query = update.callback_query

    await query.answer()

    if query.data == '1':
        await query.edit_message_text(text='topchik')
    else:
        await query.edit_message_text(text = 'enter a number from 1 to 66 \n the number == hour(s)')

async def send_memes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send memes"""
    await send_memes_runner(chat_id=update.effective_chat.id, hours = int(update.message.text))



async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """send caution if a user send unknown command"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Sorry, I didn't understand that command.")



if __name__ == '__main__':
    application = ApplicationBuilder().token(tg_access_token).build()
    

    start_handler = CommandHandler('start', start)
    memes_handler = MessageHandler(filters.Regex('^([0-66])'), send_memes)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    
    application.add_handler(start_handler)
    application.add_handler(memes_handler)
    application.add_handler(unknown_handler)
    application.add_handler(CallbackQueryHandler(button))
    
    application.run_polling()