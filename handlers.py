import types
import functools
from datetime import datetime
from colorama import Fore, Back, Style
from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove, Update,
    InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    CommandHandler, CallbackContext,
    ConversationHandler, MessageHandler,
    Filters, Updater, CallbackQueryHandler
)
from config import (
    api_key,
    api_secret,
    FAUNA_KEY,
    twilio_token,
    twilio_acc_sid
)
import cloudinary
from cloudinary.uploader import upload
from faunadb import query as q
from faunadb.client import FaunaClient
from faunadb.errors import NotFound

from twilio.rest import Client

# configure cloudinary
cloudinary.config(
    cloud_name="dp9wjhumx",
    api_key=api_key,
    api_secret=api_secret
)

# fauna client config
client = FaunaClient(secret=FAUNA_KEY)
# twilio client config
twilio_client = Client(twilio_acc_sid, twilio_token)

# Define Options
CHOOSING, DRUG_STATE, WEED_DETAILS, ALCOHOL_DETAILS, \
ALCOHOL_ROOM_NUMBER, CANCEL, ADD_PRODUCTS, BOTTLES, WEED_ROOM, \
WINE_DETAILS, WINE_ROOM_NUMBER, WINE_BOTTLES, CLASSER, BEER_BOTTLES = range(14)


def start(update, context: CallbackContext) -> int:
    print(Fore.GREEN + "Start Called ....")
    bot = context.bot
    chat_id = update.message.chat.id

    bot.send_message(
        chat_id=chat_id,
        text="Welcome to SqueakyGeezr!\n"
             "Type Hello to continue"
    )

    return CHOOSING


# get data generic user data from user and store
def choose(update, context):
    bot = context.bot
    chat_id = update.message.chat.id

    reply_keyboard = [
        [
            InlineKeyboardButton(
                text="Alcohol",
                callback_data="Alcohol"
            )],
        [
            InlineKeyboardButton(
                text="Beer",
                callback_data="Beer"
            ),
            InlineKeyboardButton(
                text="Wine",
                callback_data="Wine"
            )
        ]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    bot.send_message(
        chat_id=chat_id,
        text="Hello Good-looking! \n"
             "Pick your Dearest",
        reply_markup=markup
    )
    return DRUG_STATE


def classer(update, context):
    bot = context.bot
    chat_id = update.callback_query.message.chat.id
    a = int
    # global reply_buttons
    if update.callback_query.data == "Beer":
        weed_categories = [
            [InlineKeyboardButton("Guarana@250/="
                                  , callback_data="Guarana"),
             InlineKeyboardButton("WhiteCap@250/="
                                  , callback_data="Whitecap"),

             ]
        ]
        markup = InlineKeyboardMarkup(weed_categories, one_time_keyboard=True)
        bot.send_message(
            chat_id=chat_id,
            text="Keep a little fire burning mate,however small,however hidden",
            reply_markup=markup
        )

        return WEED_DETAILS

    elif update.callback_query.data == "Alcohol":

        bot.send_message(
            chat_id=chat_id,
            text="ALcohol may be man's worst enemy,\n"
                 "but the bible says love your enemy",
        )

        reply_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("KC Pineapple\n"
                                  "800/=", callback_data="KC"),
             InlineKeyboardButton("Flirt Vodka"
                                  "1400/=", callback_data="Flirt"),
             InlineKeyboardButton("Best Gin \n"
                                  "900/=", callback_data="Best")],

            [InlineKeyboardButton("Gilbeys \n"
                                  "1300/=", callback_data="Gilbeys"),
             InlineKeyboardButton("Konyagi \n"
                                  "700/=", callback_data="Konyagi"),
             InlineKeyboardButton("Chrome Gin\n"
                                  "800/=", callback_data="Chrome")]

        ])

        bot.send_message(
            chat_id=chat_id,
            text="What do you fancy today?",
            reply_markup=reply_buttons
        )

        return ALCOHOL_DETAILS

    wine_categories = [
        [InlineKeyboardButton("Four Cousins \n"
                              "1300/=", callback_data="Four Cousins")],

        [
            InlineKeyboardButton("Red Seasons \n"
                                 "700/=", callback_data="Red Seasons"),
            InlineKeyboardButton("Beautiful Marie\n"
                                 "800/=", callback_data="Beautiful Marie")]
    ]
    markup = InlineKeyboardMarkup(wine_categories, one_time_keyboard=True)
    bot.send_message(
        chat_id=chat_id,
        text="it's a smile, its a kiss,its a sip of wine.....it's summertime!",
    )
    bot.send_message(
        chat_id=chat_id,
        text="Tell me what you Desire",

        reply_markup=markup
    )

    return WINE_DETAILS


# Control
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Till next time Spartan',
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def weed_details(update, context):
    bot = context.bot
    chat_id = update.callback_query.message.chat.id
    chat_id2 = update.callback_query.message.chat.id

    update.callback_query.answer()
    weed_details.data = update.callback_query.data

    if update.callback_query.data == "WhiteCap" or "Guarana":
        print(Fore.MAGENTA + update.callback_query.data)

        bot.send_message(
            chat_id=chat_id2,
            text="Great choice!How many cans would you like?"
        )

        return BEER_BOTTLES

    lyft_categories = [
        [InlineKeyboardButton("Guarana@250/="
                              , callback_data="Guarana"),
         InlineKeyboardButton("Whitecap@250/="
                              , callback_data="Whitecap"),
         ]
    ]
    markup = InlineKeyboardMarkup(lyft_categories, one_time_keyboard=True)
    bot.send_message(
        chat_id=chat_id,
        text="Seems like you chose the wrong option mate!\n"
             "Try again or type /start to try something else",
        reply_markup=markup
    )
    return WEED_DETAILS


def alcohol_details(update, context):
    bot = context.bot
    chat_id = update.callback_query.message.chat.id
    chat_id2 = update.callback_query.message.chat.id

    update.callback_query.answer()
    alcohol_details.data = update.callback_query.data

    if update.callback_query.data == "KC" and "Flirt" and "Best" and "Chrome" and "Konyagi" and "Gilbeys":
        print(Fore.MAGENTA + update.callback_query.data)
        bot.send_message(
            chat_id=chat_id,
            text="Great Choice,How many bottles would you like?"
        )

        return BOTTLES

    bot.send_message(
        chat_id=chat_id,
        text="Bonkers!!Seems like you chose the wrong option,try again or type /start to try a different choice",

    )
    return ALCOHOL_DETAILS


def wine_details(update, context):
    bot = context.bot
    chat_id = update.callback_query.message.chat.id
    chat_id2 = update.callback_query.message.chat.id

    update.callback_query.answer()
    wine_details.data = update.callback_query.data

    if update.callback_query.data == "Four Cousins" or "Red Seasons" or "Beautiful Marie":
        print(Fore.MAGENTA + update.callback_query.data)
        bot.send_message(
            chat_id=chat_id,
            text="Great Choice,How many bottles would you like?"
        )

        return WINE_BOTTLES

    bot.send_message(
        chat_id=chat_id,
        text="Bonkers!!Seems like you chose the wrong option,try again or type /start to try something else",

    )
    return WINE_DETAILS


def getnumberofbottles(update, context):
    bot = context.bot
    chat_id = update.message.chat.id

    getnumberofbottles.data = update.message.text

    print(Fore.MAGENTA + getnumberofbottles.data)
    bot.send_message(
        chat_id=chat_id,
        text=f"Great! ,Enough mugging around,send me your room number or type /cancel to cancel order",
    )

    return ALCOHOL_ROOM_NUMBER


def getnumberofbeerbottles(update, context):
    bot = context.bot
    chat_id = update.message.chat.id

    getnumberofbeerbottles.data = update.message.text

    print(Fore.MAGENTA + getnumberofbeerbottles.data + "cans")
    bot.send_message(
        chat_id=chat_id,
        text=f"Great! ,Enough mugging around,send me your room number or type /cancel to cancel order",
    )

    return WEED_ROOM


def getnumberofwinebottles(update, context):
    bot = context.bot
    chat_id = update.message.chat.id

    getnumberofwinebottles.data = update.message.text

    if getnumberofwinebottles.data == "/cancel":

        return CANCEL

    elif getnumberofwinebottles.data != "/cancel":
        print(Fore.MAGENTA + getnumberofwinebottles.data)
        bot.send_message(
            chat_id=chat_id,
            text=f"Great! ,Enough mugging around,send me your room number or type /cancel to cancel order",
        )

        return WINE_ROOM_NUMBER


def getRoomNumber(update, context):
    bot = context.bot
    chat_id = update.message.chat.id
    data = update.message.text
    getRoomNumber.data = update.message.text
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")

    if getRoomNumber.data == "/cancel":

        update.message.reply_text(
            'Till next time Spartan',
            reply_markup=ReplyKeyboardRemove()
        )

    elif getRoomNumber.data != "/cancel":
        print(Fore.MAGENTA + data)
        print(Fore.YELLOW + "--COMPLETED ORDER--")
        bot.send_message(
            chat_id=chat_id,
            text="Lovely!I will be at your doorstep in a moments notice!\n"
                 "Type in /start to make another order or /cancel for a quick exit"
        )

        message = twilio_client.messages.create(
            body="Order Complete\n" + alcohol_details.data + "\n" + getnumberofbottles.data + "\n" + getRoomNumber.data + "\n" + current_time,
            from_="+17723205958",
            to="+254798945615"
        )
        print(message.sid)

        print(
            Fore.GREEN + "*-------------------------------------$$$$$$$$$$$$$$--------------------------------------------*")


def getRoomNumberWine(update, context):
    bot = context.bot
    chat_id = update.message.chat.id
    data = update.message.text
    getRoomNumberWine.data = update.message.text
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")

    if getRoomNumberWine.data == "/cancel":

        update.message.reply_text(
            'Till next time Spartan',
            reply_markup=ReplyKeyboardRemove()
        )

    elif getRoomNumberWine.data != "/cancel":
        print(Fore.MAGENTA + data)
        print(Fore.YELLOW + "--COMPLETED ORDER--")
        bot.send_message(
            chat_id=chat_id,
            text="Lovely!I will be at your doorstep in a moments notice!\n"
                 "Type in /start to make another order or /cancel for a quick exit"
        )

        message = twilio_client.messages.create(
            body="Order Complete\n" + wine_details.data + "\n" + getnumberofwinebottles.data + "\n" + getRoomNumberWine.data + "\n" + current_time,
            from_="+17723205958",
            to="+254798945615"
        )
        print(message.sid)

        print(
            Fore.GREEN + "*-------------------------------------$$$$$$$$$$$$$$--------------------------------------------*")


def getRoomNumberWeed(update, context):
    bot = context.bot
    chat_id = update.message.chat.id
    data = update.message.text
    getRoomNumberWeed.data = update.message.text
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")

    if getRoomNumberWeed.data == "/cancel":

        update.message.reply_text(
            'Till next time Spartan',
            reply_markup=ReplyKeyboardRemove()
        )

    elif getRoomNumberWeed.data != "/cancel":
        print(data)
        print(Fore.YELLOW + "--COMPLETED ORDER--")
        bot.send_message(
            chat_id=chat_id,
            text="Lovely!I will be at your doorstep in a moments notice!\n"
                 "Type in /start to make another order or /cancel for a quick exit"
        )

        message = twilio_client.messages.create(
            body="Order Complete\n" + weed_details.data + "\n" + getnumberofbeerbottles.data + " cans\n" + getRoomNumberWeed.data + "\n" + current_time,
            from_="+17723205958",
            to="+254798945615"
        )
        print(message.sid)

        print(
            Fore.GREEN + "*-------------------------------------$$$$$$$$$$$$$$--------------------------------------------*")
