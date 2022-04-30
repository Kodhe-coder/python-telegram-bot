import handlers
from colorama import Fore, Back, Style
from telegram.ext import (
    CommandHandler, CallbackContext,
    ConversationHandler, MessageHandler,
    Filters, Updater, CallbackQueryHandler
)
from config import TOKEN

updater = Updater(token=TOKEN, use_context=True)
print(updater)
dispatcher = updater.dispatcher


def main():
    print(Fore.RED + "BOT STARTED ...")
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handlers.start)],
        states={
            handlers.CHOOSING: [
                MessageHandler(
                    Filters.all, handlers.choose
                )
            ],
            handlers.CANCEL: [
                CallbackQueryHandler(handlers.cancel)
            ],


            handlers.DRUG_STATE: [
                CallbackQueryHandler(handlers.classer)
            ],
            handlers.WEED_DETAILS: [
                CallbackQueryHandler(handlers.weed_details)
            ],
            handlers.ALCOHOL_DETAILS: [
                CallbackQueryHandler(handlers.alcohol_details)
            ],
            handlers.WINE_DETAILS: [
                CallbackQueryHandler(handlers.wine_details)
            ],

            handlers.BOTTLES: [
                MessageHandler(
                    Filters.all, handlers.getnumberofbottles
                )
            ],

            handlers.BEER_BOTTLES: [
                MessageHandler(
                    Filters.all, handlers.getnumberofbeerbottles
                )
            ],

            handlers.WINE_BOTTLES: [
                MessageHandler(
                    Filters.all, handlers.getnumberofwinebottles
                )
            ],

            handlers.WEED_ROOM: [
                MessageHandler(
                    Filters.all, handlers.getRoomNumberWeed
                )
            ],


            handlers.ALCOHOL_ROOM_NUMBER: [
                MessageHandler(
                    Filters.all, handlers.getRoomNumber
                )
            ],

            handlers.WINE_ROOM_NUMBER: [
                MessageHandler(
                    Filters.all, handlers.getRoomNumberWine
                )
            ]

        },
        fallbacks=[CommandHandler('cancel', handlers.cancel)],
        allow_reentry=True
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    try:
        main()
    except:
        print('There is a network problem')

    # main()
