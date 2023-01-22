from telegram import *
from telegram.ext import *

from ontology.recipes_ontology import RecipesOntology

from bot.recipes_conversation_handler import RecipesConversationHandler

class TelegramBot:
    def __init__(self, token, ontology: RecipesOntology):
        self.updater = Updater(token, use_context=True)
        self.ontology = ontology

        dispatcher = self.updater.dispatcher

        dispatcher.add_handler(CommandHandler('start', callback=self.start_cmd))
        dispatcher.add_handler(CommandHandler('help', callback=self.help_cmd))
        dispatcher.add_handler(CommandHandler('sparql', callback=self.sparql_cmd))

        dispatcher.add_handler(RecipesConversationHandler(ontology))

    def start(self):
        print("Recipes bot starting ...")
        self.updater.start_polling()
        print("Recipes bot started!")
        self.updater.idle()
    
    def start_cmd(self, update: Update, context: CallbackContext):
        update.message.reply_text("Hey!")

    def sparql_cmd(self, update: Update, context: CallbackContext):
        text = update.message.text
        query = text[len("/sparql")::]
        result = list(self.ontology.run_query(query))
        if len(result) == 0:
            update.message.reply_text("No results for the given query")
            return
        page_size = 20
        paged_result = [result[i:i + page_size] for i in range(0, len(result), page_size)]
        for page in paged_result:
            response_message = ""
            for x in page:
                response_message += str(x) + "\n"
            update.message.reply_text(response_message)

    def help_cmd(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            """
/start -> starts the bot
/help -> lists the commands
/recipe -> chooses a recipe
"""
        )
