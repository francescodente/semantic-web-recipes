from telegram import *
from telegram.ext import *

from bot import bot_states
from bot import bot_events

from bot.state.chat_state import ChatState

class TelegramBot:
    def __init__(self, token):
        self.updater = Updater(token, use_context=True)
        self.chat_states = {}

        dispatcher = self.updater.dispatcher

        dispatcher.add_handler(CommandHandler('start', callback=self.start_cmd))
        dispatcher.add_handler(CommandHandler('help', callback=self.help_cmd))

        dispatcher.add_handler(ConversationHandler(
            entry_points=[
                CommandHandler('recipe', callback=self.recipe_cmd)
            ],
            states={
                bot_states.INITIAL: [
                    CallbackQueryHandler(callback=self.select_ingredients, pattern=bot_events.SELECT_INGREDIENTS),
                    CallbackQueryHandler(callback=self.select_origin, pattern=bot_events.SELECT_ORIGIN),
                ],
                bot_states.SELECTING_INGREDIENTS: [

                ],
                bot_states.SELECTING_ORIGIN: [
                    CallbackQueryHandler(callback=self.origin_selected)
                ]
            },
            fallbacks=[

            ]
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

    def recipe_cmd(self, update: Update, context: CallbackContext):
        chat_state = self.get_or_create_chat_state(update)
        self.send_main_message(context, chat_state)
        return bot_states.INITIAL
    
    def select_ingredients(self, update: Update, context: CallbackContext):
        
        return bot_states.SELECTING_INGREDIENTS
    
    def select_origin(self, update: Update, context: CallbackContext):
        known_countries = [
            'Italy',
            'France',
            'Spain',
            'Japan',
        ]
        context.bot.send_message(
            update.effective_chat.id,
            "Which dish origin would you prefer?",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text=country, callback_data=country)] for country in known_countries]
            )
        )
        return bot_states.SELECTING_ORIGIN
    
    def origin_selected(self, update: Update, context: CallbackContext):
        country = update.callback_query.data
        chat_state = self.get_or_create_chat_state(update)
        chat_state.set_selected_country(country)
        self.send_main_message(context, chat_state)
        return bot_states.INITIAL
    
    def get_or_create_chat_state(self, update: Update) -> ChatState:
        chat_id = update.effective_chat.id
        if not chat_id in self.chat_states:
            self.chat_states[chat_id] = ChatState(chat_id)
        return self.chat_states[chat_id]
    
    def send_main_message(self, context: CallbackContext, chat_state: ChatState):
        context.bot.send_message(
            chat_state.id,
            "Hey there! Where do you want to start finding the best recipe for you?",
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(text="Ingredients", callback_data=bot_events.SELECT_INGREDIENTS)],
                [InlineKeyboardButton(text="Origin", callback_data=bot_events.SELECT_ORIGIN)],
            ])
        )

