from telegram.ext import Updater
from telegram.ext import CommandHandler

Token = "5831078632:AAEU8w680srvoI58qU3myp7OxKlBYd3vzt0"
updater = Updater("5831078632:AAEU8w680srvoI58qU3myp7OxKlBYd3vzt0", use_context=True)

dispatcher = updater.dispatcher


def start_cmd(update, context):
    update.message.reply_text("Hey!")


def help_cmd(update, context):
    update.message.reply_text("""
    /start -> starts the bot
/help -> lists the commands
/recipe -> chooses a recipe  
    """)


def recipe_cmd(update, context):
    update.message.reply_text("Here is your recipe")


dispatcher.add_handler(CommandHandler('start', start_cmd))
dispatcher.add_handler(CommandHandler('help', help_cmd))
dispatcher.add_handler(CommandHandler('recipe', recipe_cmd))

updater.start_polling()
updater.idle()


