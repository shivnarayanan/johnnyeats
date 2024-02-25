import random
import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

from src.database_utils import get_places, get_outlets

load_dotenv(override=True)

TOKEN = os.environ.get('BOT_TOKEN')

last_suggested_place = [None]

def start(update: Update, context: CallbackContext) -> None:
    if update.callback_query:
        query = update.callback_query
        keyboard = [
            [InlineKeyboardButton("Place Suggestion", callback_data='place')],
            [InlineKeyboardButton("Browse All Places", callback_data='-')],
            [InlineKeyboardButton("Provide Feedback", callback_data='-')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.edit_text('What would you like Johnny to assist you with?', reply_markup=reply_markup)
    else:
        keyboard = [
            [InlineKeyboardButton("Place Suggestion", callback_data='place')],
            [InlineKeyboardButton("Browse All Places", callback_data='-')],
            [InlineKeyboardButton("Provide Feedback", callback_data='-')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('What would you like Johnny to assist you with?', reply_markup=reply_markup)

def escape_special_characters(message):
    special_characters = r'\-`_{}[]()#+.!'
    escaped_message = ''.join(['\\' + char if char in special_characters else char for char in message])
    return escaped_message

def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if query.data == 'place':
        place_suggestions = get_places()

        place = random.choice([place for place in place_suggestions if place != last_suggested_place[0]])

        last_suggested_place[0] = place 

        keyboard = [
            [InlineKeyboardButton("View Food Outlets", callback_data='view_food_outlets')],
            [InlineKeyboardButton("Suggest Another Place", callback_data='place')],
            [InlineKeyboardButton("Go Back to Main Menu", callback_data='start')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        text = f"Let's go *{place}*\!\n\nClick on View Food Outlets to see a list of food outlets at *{place}*\."
        
        query.edit_message_text(text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif query.data == 'view_food_outlets':
        suggested_place = last_suggested_place[0]
        food_outlets = get_outlets(suggested_place)

        text = f"Food outlets at *{suggested_place}*:\n\n"
        text += "\n".join(food_outlets)
        text = escape_special_characters(text)

        keyboard = [
            [InlineKeyboardButton("Suggest Another Place", callback_data='place')],
            [InlineKeyboardButton("Go Back to Main Menu", callback_data='start')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif query.data == 'start':
        start(update, context)

def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_click))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
