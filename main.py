import random
import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

load_dotenv(override=True)

TOKEN = os.environ.get('BOT_TOKEN')

last_suggested_place = [None]

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Food Suggestion", callback_data='food')],
        [InlineKeyboardButton("Drink Suggestion", callback_data='food')],
        [InlineKeyboardButton("Place Suggestion", callback_data='place')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('What suggestion would you like to receive from Johnny today?', reply_markup=reply_markup)

def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'food':
        food_suggestions = [
            "Pizza",
            "Burger",
            "Sushi",
            "Tacos",
        ]

        food = random.choice(food_suggestions)
        query.edit_message_text(f"How about trying {food}?")
    elif query.data == 'place':
        place_suggestions = ["Marina One", "Food Garden", "Lau Pa Sat", "Hong Leong Bldg"]

        place = random.choice([place for place in place_suggestions if place != last_suggested_place[0]])

        last_suggested_place[0] = place 

        keyboard = [
            [InlineKeyboardButton("Suggest Another Place", callback_data='place')],
            [InlineKeyboardButton("View Food Outlets", callback_data='view_food_outlets')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        text = f"How about {place}?\n\nClick on <b>View Food Outlets</b> to see a list of food outlets at {place}."
        
        query.edit_message_text(text, reply_markup=reply_markup, parse_mode="html")

    elif query.data == 'view_food_outlets':
        # Fetch the originally suggested place
        suggested_place = last_suggested_place[0]

        # TODO: Add logic to display the list of food outlets based on the suggested_place
        # Example: Fetch a list of food outlets from a database or other source

        # For demonstration purposes, let's create a sample list.
        food_outlets = ["Restaurant 1", "Restaurant 2", "Restaurant 3"]

        text = f"Food outlets at {suggested_place}:\n\n"
        text += "\n".join(food_outlets)

        query.edit_message_text(text)

def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_click))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
