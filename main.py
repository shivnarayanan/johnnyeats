import random
import os

import re
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters

from src.database_utils import get_places, get_outlets
from src.github_utils import create_issue

load_dotenv(override=True)

TOKEN = os.environ.get('BOT_TOKEN')

last_suggested_place = [None]
feedback_subject = {}

def start(update: Update, context: CallbackContext) -> None:
    if update.callback_query:
        query = update.callback_query
        keyboard = [
            [InlineKeyboardButton("Place Suggestion", callback_data='place')],
            [InlineKeyboardButton("Browse All Places", callback_data='browse_all_places')],
            [InlineKeyboardButton("Provide Feedback", callback_data='provide_feedback')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.edit_text('What would you like Johnny to assist you with?', reply_markup=reply_markup)
    else:
        keyboard = [
            [InlineKeyboardButton("Place Suggestion", callback_data='place')],
            [InlineKeyboardButton("Browse All Places", callback_data='browse_all_places')],
            [InlineKeyboardButton("Provide Feedback", callback_data='provide_feedback')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('What would you like Johnny to assist you with?', reply_markup=reply_markup)

def escape_special_characters(message):
    special_characters = r'\-`{}[]()#+.!'
    escaped_message = ''.join(['\\' + char if char in special_characters else char for char in message])
    return escaped_message

def capture_feedback(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_chat.id
    username = (update.effective_user.username.capitalize() if update.effective_user.username else None)

    keyboard = [
            [InlineKeyboardButton("Go Back to Main Menu", callback_data='start')]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if context.user_data.get('awaiting_feedback_subject', False):
        subject = update.message.text
        feedback_subject[user_id] = subject

        text = "📝 Thank you! Now, please provide your detailed feedback. \n\nBe as descriptive as possible to help us understand your feedback better."  
        update.message.reply_text(text)
        context.user_data['awaiting_detailed_feedback'] = True

        del context.user_data['awaiting_feedback_subject']
    elif context.user_data.get('awaiting_detailed_feedback', False):
        detailed_feedback = update.message.text
        user_feedback = {
            'subject': feedback_subject.get(user_id, 'No subject provided'),
            'detailed_feedback': detailed_feedback
        }
        print("User feedback:", user_feedback)
        
        create_issue(user_feedback['subject'], user_feedback['detailed_feedback'])
        
        text = f"Thank you for your feedback, {username}! It has been noted and we will follow up within 24h. 😊"
        update.message.reply_text(text, reply_markup=reply_markup)

        del context.user_data['awaiting_detailed_feedback']
    else:
        text = "What would you like Johnny to assist you with?"
        update.message.reply_text(escape_special_characters(text))

def view_food_outlets(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    place = query.data.split('_')[2]  # Extract place name from callback_data
    food_outlets = get_outlets(place)

    text = f"Food outlets at {place}:\n\n"
    text += "\n".join(food_outlets)
    query.edit_message_text(text)

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

    elif query.data == 'provide_feedback':
        text = "📝 Please provide a subject/title for your feedback. \n\nFor example: _Inaccurate Eatery Information_"
        keyboard = [
            [InlineKeyboardButton("Go Back to Main Menu", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(escape_special_characters(text), reply_markup=reply_markup, parse_mode="MarkdownV2")

        context.user_data['awaiting_feedback_subject'] = True

    elif query.data == 'browse_all_places':
        print("Browse all places button clicked")  
        try:
            places = get_places()
            print("Places:", places) 
            buttons = [[InlineKeyboardButton(place, callback_data=f'view_food_outlets_{place}')] for place in places]
            keyboard = buttons + [[InlineKeyboardButton("Go Back to Main Menu", callback_data='start')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text("Choose a place:", reply_markup=reply_markup)
        except Exception as e:
            print("Error fetching places:", e)

    elif re.match(r'^view_food_outlets_.*$', query.data):
        requested_place = query.data.split('_')[-1]
        food_outlets = get_outlets(requested_place)

        text = f"Food outlets at *{requested_place}*:\n\n"
        text += "\n".join(food_outlets)
        text = escape_special_characters(text)

        keyboard = [
            [InlineKeyboardButton("Go Back to All Places", callback_data='browse_all_places')],
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
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, capture_feedback))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
