from telegram import *
from telegram.ext import *

from ontology.recipes_ontology import RecipesOntology

from bot.recipes_conversation_handler import RecipesConversationHandler

class TelegramBot:
    def __init__(self, token, ontology: RecipesOntology):
        self.updater = Updater(token, use_context=True)

        dispatcher = self.updater.dispatcher

        dispatcher.add_handler(CommandHandler('start', callback=self.start_cmd))
        dispatcher.add_handler(CommandHandler('help', callback=self.help_cmd))

        dispatcher.add_handler(RecipesConversationHandler(ontology))

    def start(self):
        print("Recipes bot starting ...")
        self.updater.start_polling()
        print("Recipes bot started!")
        self.updater.idle()
    
    def start_cmd(self, update: Update, context: CallbackContext):
        update.message.reply_text("Hey!")

    def help_cmd(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            """
/start -> starts the bot
/help -> lists the commands
/recipe -> chooses a recipe
"""
        )
