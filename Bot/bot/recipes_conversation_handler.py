from telegram import *
from telegram.ext import *
from telegram.ext.callbackqueryhandler import RT

from bot import bot_states
from bot import bot_events
from bot.state.chat_state import ChatState
from ontology.recipes_ontology import RecipesOntology
from ontology.model import *
from typing import Callable

class RecipesConversationHandler(ConversationHandler):
    def __init__(self):
        super(RecipesConversationHandler, self).__init__(
            entry_points=[
                CommandHandler('recipe', self.with_chat_state(callback=self.begin))
            ],
            states={
                bot_states.INITIAL: [
                    CallbackQueryHandler(callback=self.with_chat_state(self.request_ingredients), pattern=bot_events.SELECT_INGREDIENTS),
                    CallbackQueryHandler(callback=self.with_chat_state(self.show_available_origins), pattern=bot_events.SELECT_ORIGIN),
                    CallbackQueryHandler(callback=self.with_chat_state(self.show_suitable_recipes), pattern=bot_events.SELECT_RECIPE),
                ],
                bot_states.SELECTING_INGREDIENTS: [
                    CallbackQueryHandler(callback=self.go_back(bot_states.INITIAL), pattern=bot_events.BACK),
                    MessageHandler(callback=self.with_chat_state(self.ingredients_selected), filters=Filters.text),
                ],
                bot_states.SELECTING_ORIGIN: [
                    CallbackQueryHandler(callback=self.go_back(bot_states.INITIAL), pattern=bot_events.BACK),
                    CallbackQueryHandler(callback=self.with_chat_state(self.origin_selected)),
                ],
                bot_states.SELECTING_RECIPE: [
                    CallbackQueryHandler(callback=self.go_back(bot_states.INITIAL), pattern=bot_events.BACK),
                    CallbackQueryHandler(callback=self.with_chat_state(self.recipe_selected)),
                ],
                bot_states.VIEWING_RECIPE: [
                    CallbackQueryHandler(callback=self.go_back(bot_states.SELECTING_RECIPE), pattern=bot_events.BACK),
                    CallbackQueryHandler(callback=self.with_chat_state(self.view_recipe_steps), pattern=bot_events.VIEW_STEPS),
                ],
                bot_states.VIEWING_STEPS: [
                    CallbackQueryHandler(callback=self.with_chat_state(self.next_step), pattern=bot_events.NEXT),
                    CallbackQueryHandler(callback=self.with_chat_state(self.prev_step), pattern=bot_events.PREV),
                    CallbackQueryHandler(callback=self.go_back(bot_states.VIEWING_RECIPE), pattern=bot_events.BACK),
                ]
            },
            fallbacks=[]
        )
        self.ontology = RecipesOntology()
        self.chat_states = {}
    
    def with_chat_state(self, callback: Callable[[ChatState, Update, CallbackContext], RT]) -> Callable[[Update, CallbackContext], RT]:
        def f(update: Update, context: CallbackContext):
            chat_state = self.get_or_create_chat_state(update)
            return callback(chat_state, update, context)
        return f
    
    def get_or_create_chat_state(self, update: Update) -> ChatState:
        chat_id = update.effective_chat.id
        if not chat_id in self.chat_states:
            self.chat_states[chat_id] = ChatState(chat_id)
        return self.chat_states[chat_id]
    
    def main_menu_markup(self, chat_state: ChatState) -> InlineKeyboardMarkup:
        selected_country = chat_state.get_selected_country()
        selected_country_text = selected_country if selected_country else "None selected"

        ingredients = chat_state.get_selected_ingredients()
        selected_ingredients_text = ", ".join(ingredients) if len(ingredients) > 0 else "None selected"

        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="GO ➡️", callback_data=bot_events.SELECT_RECIPE)],
            [InlineKeyboardButton(text=f"Ingredients: {selected_ingredients_text}", callback_data=bot_events.SELECT_INGREDIENTS)],
            [InlineKeyboardButton(text=f"Origin: {selected_country_text}", callback_data=bot_events.SELECT_ORIGIN)],
        ])

    def begin(self, chat_state: ChatState, _: Update, context: CallbackContext):
        chat_state.push_message(
            context,
            "Hey there! Where do you want to start finding the best recipe for you?",
            reply_markup=self.main_menu_markup(chat_state)
        )
        return bot_states.INITIAL
    
    def go_back(self, state: str) -> Callable[[Update, CallbackContext], RT]:
        def go_back_impl(chat_state: ChatState):
            chat_state.pop_message()
            return state
        return self.with_chat_state(lambda s, u, c: go_back_impl(s))

    def request_ingredients(self, chat_state: ChatState, update: Update, context: CallbackContext):
        update.callback_query.answer()
        chat_state.push_message(
            context,
            "Send me a message with your available ingredients, each on a different line",
            reply_markup=InlineKeyboardMarkup([[self.back_button()]])
        )
        return bot_states.SELECTING_INGREDIENTS
    
    def ingredients_selected(self, chat_state: ChatState, update: Update, _: CallbackContext):
        lines = update.message.text.splitlines()
        chat_state.set_selected_ingredients(lines)
        update.message.delete()
        chat_state.pop_message()
        chat_state.last_message().edit_reply_markup(self.main_menu_markup(chat_state))
        return bot_states.INITIAL
    
    def show_available_origins(self, chat_state: ChatState, update: Update, context: CallbackContext):
        update.callback_query.answer()
        known_countries = self.ontology.get_countries()
        chat_state.push_message(
            context,
            "Which dish origin would you prefer?",
            reply_markup=InlineKeyboardMarkup([
                [self.back_button()],
                *[[InlineKeyboardButton(text=country.name, callback_data=country.name)] for country in known_countries],
            ])
        )
        return bot_states.SELECTING_ORIGIN
    
    def origin_selected(self, chat_state: ChatState, update: Update, _: CallbackContext):
        update.callback_query.answer()
        country = update.callback_query.data
        chat_state.set_selected_country(country)
        chat_state.pop_message()
        chat_state.last_message().edit_reply_markup(self.main_menu_markup(chat_state))
        return bot_states.INITIAL

    def show_suitable_recipes(self, chat_state: ChatState, update: Update, context: CallbackContext):
        update.callback_query.answer()
        found_recipes = self.ontology.find_recipes(chat_state)
        chat_state.set_recipes(found_recipes)
        chat_state.push_message(
            context,
            "Here's what I found! Select any recipe to view its details",
            reply_markup=InlineKeyboardMarkup([
                [self.back_button()],
                *[[InlineKeyboardButton(text=recipe.name, callback_data=recipe.name)] for recipe in found_recipes],
            ])
        )
        return bot_states.SELECTING_RECIPE

    def recipe_selected(self, chat_state: ChatState, update: Update, context: CallbackContext):
        update.callback_query.answer()
        recipe = chat_state.get_recipe(update.callback_query.data)
        chat_state.set_selected_recipe(recipe)
        chat_state.push_message(
            context,
            f"*{recipe.name}*",
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="View steps", callback_data=bot_events.VIEW_STEPS)],
                [self.back_button()],
            ])
        )
        return bot_states.VIEWING_RECIPE

    def back_button(self):
        return InlineKeyboardButton(text="Go back", callback_data=bot_events.BACK)
    
    def view_recipe_steps(self, chat_state: ChatState, update: Update, context: CallbackContext):
        update.callback_query.answer()
        recipe = chat_state.get_selected_recipe()
        step = self.ontology.find_step(recipe.initialStep)
        chat_state.change_step(step, 0)
        chat_state.push_message(
            context,
            self.create_step_text(step, 0),
            reply_markup=self.step_buttons(step),
            parse_mode=ParseMode.MARKDOWN_V2
        )
        return bot_states.VIEWING_STEPS
    
    def next_step(self, chat_state: ChatState, update: Update, context: CallbackContext):
        return self.change_step(chat_state, update, lambda s : s.next, lambda x: x + 1)

    def prev_step(self, chat_state: ChatState, update: Update, context: CallbackContext):
        return self.change_step(chat_state, update, lambda s : s.prev, lambda x: x - 1)

    def change_step(self, chat_state: ChatState, update: Update, get_step_id: Callable[[Step], int], update_index: Callable[[int], int]):
        update.callback_query.answer()
        step_id = get_step_id(chat_state.get_current_step())
        index = update_index(chat_state.get_step_index())
        step = self.ontology.find_step(step_id)
        chat_state.change_step(step, index)
        chat_state.last_message().edit_text(self.create_step_text(step, index), parse_mode=ParseMode.MARKDOWN_V2)
        chat_state.last_message().edit_reply_markup(self.step_buttons(step))
        return bot_states.VIEWING_STEPS
    
    def create_step_text(self, step: Step, index: int) -> str:
        return f"""
*Step {index}*

{step.description}
"""
    
    def step_buttons(self, step: Step):
        buttons = [[self.back_button()]]
        if step.next is not None:
            buttons.append([InlineKeyboardButton(text="➡️", callback_data=bot_events.NEXT)])
        if step.prev is not None:
            buttons.append([InlineKeyboardButton(text="⬅️", callback_data=bot_events.PREV)])
        return InlineKeyboardMarkup(buttons)