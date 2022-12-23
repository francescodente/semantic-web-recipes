from telegram import *
from telegram.ext import *

from bot import bot_states
from bot import bot_events
from bot.state.chat_state import ChatState

class RecipesConversationHandler:
    def __init__(self):
        self.chat_states = {}

    def begin(self, update: Update, context: CallbackContext):
        chat_state = self.get_or_create_chat_state(update)
        self.send_main_message(context, chat_state)
        return bot_states.INITIAL

    def select_ingredients(self, update: Update, context: CallbackContext):
        context.bot.send_message(
            update.effective_chat.id,
            "Send me a message with your available ingredients, each on a different line")
        return bot_states.SELECTING_INGREDIENTS
    
    def ingredients_selected(self, update: Update, context: CallbackContext):
        chat_state = self.get_or_create_chat_state(update)
        lines = update.message.text.splitlines()
        chat_state.set_selected_ingredients(lines)
        self.send_main_message(context, chat_state)
        return bot_states.INITIAL
    
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
        selected_country = chat_state.get_selected_country()
        selected_country_text = selected_country if selected_country != None else "None selected"

        ingredients = chat_state.get_selected_ingredients()
        selected_ingredients_text = ", ".join(ingredients) if len(ingredients) > 0 else "None selected"

        context.bot.send_message(
            chat_state.id,
            "Hey there! Where do you want to start finding the best recipe for you?",
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(text=f"Ingredients: {selected_ingredients_text}", callback_data=bot_events.SELECT_INGREDIENTS)],
                [InlineKeyboardButton(text=f"Origin: {selected_country_text}", callback_data=bot_events.SELECT_ORIGIN)],
            ])
        )