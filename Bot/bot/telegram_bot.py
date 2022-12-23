from telegram import *
from telegram.ext import *

from bot import bot_states
from bot import bot_events

from bot.recipes_conversation_handler import RecipesConversationHandler

class TelegramBot:
    def __init__(self, token):
        self.updater = Updater(token, use_context=True)

        recipes_handler = RecipesConversationHandler()

        dispatcher = self.updater.dispatcher

        dispatcher.add_handler(CommandHandler('start', callback=self.start_cmd))
        dispatcher.add_handler(CommandHandler('help', callback=self.help_cmd))

        dispatcher.add_handler(ConversationHandler(
            entry_points=[
                CommandHandler('recipe', callback=recipes_handler.begin)
            ],
            states={
                bot_states.INITIAL: [
                    CallbackQueryHandler(callback=recipes_handler.select_ingredients, pattern=bot_events.SELECT_INGREDIENTS),
                    CallbackQueryHandler(callback=recipes_handler.select_origin, pattern=bot_events.SELECT_ORIGIN),
                ],
                bot_states.SELECTING_INGREDIENTS: [
                    MessageHandler(callback=recipes_handler.ingredients_selected, filters=Filters.text)
                ],
                bot_states.SELECTING_ORIGIN: [
                    CallbackQueryHandler(callback=recipes_handler.origin_selected)
                ]
            },
            fallbacks=[]
        ))

    def start(self):
        print("Recipes bot starting ...")
        self.updater.start_polling()
        print("Recipes bot started!")
        self.updater.idle()
    
    def start_cmd(self, update: Update, context: CallbackContext):
        update.message.reply_text("Hey!")

    def help_cmd(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            """/start -> starts the bot
        /help -> lists the commands
        /recipe -> chooses a recipe"""
        )
