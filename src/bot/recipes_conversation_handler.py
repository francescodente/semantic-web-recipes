from telegram import *
from telegram.ext import *
from telegram.ext.callbackqueryhandler import RT

from bot import bot_states
from bot import bot_events
from bot.state.chat_state import ChatState
from ontology.recipes_ontology import RecipesOntology
from ontology.model import *
from typing import Callable

from bot.utils.telegram_utils import escape_text

class RecipesConversationHandler(ConversationHandler):
    def __init__(self, ontology: RecipesOntology):
        super(RecipesConversationHandler, self).__init__(
            entry_points=[
                CommandHandler('recipe', self.with_chat_state(callback=self.begin))
            ],
            states={
                bot_states.INITIAL: [
                    CallbackQueryHandler(callback=self.with_chat_state(self.request_ingredients), pattern=bot_events.SELECT_INGREDIENTS),
                    CallbackQueryHandler(callback=self.with_chat_state(self.show_available_origins), pattern=bot_events.SELECT_ORIGIN),
                    CallbackQueryHandler(callback=self.with_chat_state(self.show_suitable_dishes), pattern=bot_events.SELECT_DISH),
                    CallbackQueryHandler(callback=self.with_chat_state(self.toggle_vegan), pattern=bot_events.TOGGLE_VEGAN),
                ],
                bot_states.SELECTING_INGREDIENTS: [
                    CallbackQueryHandler(callback=self.go_back(bot_states.INITIAL), pattern=bot_events.BACK),
                    MessageHandler(callback=self.with_chat_state(self.ingredients_selected), filters=Filters.text),
                ],
                bot_states.SELECTING_ORIGIN: [
                    CallbackQueryHandler(callback=self.go_back(bot_states.INITIAL), pattern=bot_events.BACK),
                    CallbackQueryHandler(callback=self.with_chat_state(self.origin_selected)),
                ],
                bot_states.SELECTING_DISH: [
                    CallbackQueryHandler(callback=self.go_back(bot_states.INITIAL), pattern=bot_events.BACK),
                    CallbackQueryHandler(callback=self.with_chat_state(self.dish_selected)),
                ], 
                bot_states.SELECTING_RECIPE: [
                    CallbackQueryHandler(callback=self.go_back(bot_states.SELECTING_DISH), pattern=bot_events.BACK),
                    CallbackQueryHandler(callback=self.with_chat_state(self.recipe_selected)),
                ],
                bot_states.VIEWING_RECIPE: [
                    CallbackQueryHandler(callback=self.go_back(bot_states.SELECTING_RECIPE), pattern=bot_events.BACK),
                    CallbackQueryHandler(callback=self.with_chat_state(self.view_recipe_steps), pattern=bot_events.VIEW_STEPS),
                ],
                bot_states.VIEWING_STEPS: [
                    CallbackQueryHandler(callback=self.go_back(bot_states.VIEWING_RECIPE), pattern=bot_events.BACK),
                    CallbackQueryHandler(callback=self.with_chat_state(self.next_step), pattern=bot_events.NEXT),
                    CallbackQueryHandler(callback=self.with_chat_state(self.prev_step), pattern=bot_events.PREV),
                ]
            },
            fallbacks=[]
        )
        self.ontology = ontology
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
        selected_country = chat_state.selected_country
        selected_country_text = selected_country.name if selected_country else "None selected"

        ingredients = chat_state.selected_ingredients
        selected_ingredients_text = ", ".join(ingredients) if len(ingredients) > 0 else "None selected"

        vegan_icon = "✅" if chat_state.vegan else "❌"

        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="GO ➡️", callback_data=bot_events.SELECT_DISH)],
            [InlineKeyboardButton(text=f"Ingredients: {selected_ingredients_text}", callback_data=bot_events.SELECT_INGREDIENTS)],
            [InlineKeyboardButton(text=f"Origin: {selected_country_text}", callback_data=bot_events.SELECT_ORIGIN)],
            [InlineKeyboardButton(text=f"Vegan? {vegan_icon}", callback_data=bot_events.TOGGLE_VEGAN)],
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
        def country_button(i: int, country: Country) -> InlineKeyboardButton:
            return InlineKeyboardButton(
                text=f"""{country.name} ({country.recipes} {"recipe" if country.recipes == 1 else "recipes"})""",
                callback_data=i
            )
        update.callback_query.answer()
        countries = self.ontology.get_countries_with_at_least_one_dish()
        chat_state.remember_countries(countries)
        chat_state.push_message(
            context,
            "Which dish origin would you prefer?",
            reply_markup=InlineKeyboardMarkup([
                [self.back_button()],
                *[[country_button(i, country)] for i, country in enumerate(countries)],
            ])
        )
        return bot_states.SELECTING_ORIGIN
    
    def origin_selected(self, chat_state: ChatState, update: Update, _: CallbackContext):
        update.callback_query.answer()
        country_index = int(update.callback_query.data)
        chat_state.set_selected_country(country_index)
        chat_state.pop_message()
        chat_state.last_message().edit_reply_markup(self.main_menu_markup(chat_state))
        return bot_states.INITIAL

    def toggle_vegan(self, chat_state: ChatState, update: Update, _: CallbackContext):
        update.callback_query.answer()
        chat_state.toggle_vegan()
        chat_state.last_message().edit_reply_markup(self.main_menu_markup(chat_state))
        return bot_states.INITIAL

    def show_suitable_dishes(self, chat_state: ChatState, update: Update, context: CallbackContext):
        def dish_button(i: int, dish: Dish) -> InlineKeyboardButton:
            return InlineKeyboardButton(text=dish.name, callback_data=i)

        update.callback_query.answer()
        found_dishes = self.ontology.find_dishes(chat_state)
        chat_state.set_search_result(found_dishes)
        chat_state.push_message(
            context,
            "Here's what I found! Select any dish to view the corresponding recipes",
            reply_markup=InlineKeyboardMarkup([
                [self.back_button()],
                *[[dish_button(i, dish)] for i, dish in enumerate(found_dishes)],
            ])
        )
        return bot_states.SELECTING_DISH

    def dish_selected(self, chat_state: ChatState, update: Update, context: CallbackContext):
        def recipe_button(i: int, recipe: Recipe) -> InlineKeyboardButton:
            return InlineKeyboardButton(text=f"{recipe.title} ({recipe.difficulty})", callback_data=i)
        
        update.callback_query.answer()
        dish = chat_state.get_dish_from_search_result(int(update.callback_query.data))
        chat_state.set_selected_dish(dish)
        chat_state.push_message(
            context,
            f"Here are the available recipes for '{dish.name}'",
            reply_markup=InlineKeyboardMarkup([
                [self.back_button()],
                *[[recipe_button(i, recipe)] for i, recipe in enumerate(dish.recipes)],
            ])
        )
        return bot_states.SELECTING_RECIPE
    
    def recipe_selected(self, chat_state: ChatState, update: Update, context: CallbackContext):
        def show_ingredient(ingredient: Ingredient) -> str:
            return f"• *{ingredient.quantity}* {ingredient.unit} of {ingredient.name}"

        def show_ingredients(ingredients: list[Ingredient]) -> str:
            return "\n".join(map(show_ingredient, ingredients))
            
        update.callback_query.answer()
        dish = chat_state.selected_dish
        recipe = dish.recipes[int(update.callback_query.data)]
        chat_state.set_selected_recipe(recipe)
        ingredients = self.ontology.find_recipe_ingredients(recipe.iri)
        chat_state.push_message(
            context,
            escape_text(f"""
*{recipe.title}*

*Preparation time*: {recipe.preparation_time}
*Difficulty*: {recipe.difficulty}

{show_ingredients(ingredients)}
"""),
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=InlineKeyboardMarkup([
                [self.back_button()],
                [InlineKeyboardButton(text="View steps", callback_data=bot_events.VIEW_STEPS)],
            ])
        )
        return bot_states.VIEWING_RECIPE

    def back_button(self):
        return InlineKeyboardButton(text="⬆️ Go back ⬆️", callback_data=bot_events.BACK)
    
    def view_recipe_steps(self, chat_state: ChatState, update: Update, context: CallbackContext):
        update.callback_query.answer()
        recipe = chat_state.selected_recipe
        step = recipe.initial_step
        chat_state.change_step(step, 0)
        chat_state.push_message(
            context,
            self.create_step_text(step, 0),
            reply_markup=self.step_buttons(step),
            parse_mode=ParseMode.MARKDOWN_V2
        )
        return bot_states.VIEWING_STEPS
    
    def next_step(self, chat_state: ChatState, update: Update, _: CallbackContext):
        return self.change_step(chat_state, update, lambda s : s.hasNext, lambda x: x + 1)

    def prev_step(self, chat_state: ChatState, update: Update, _: CallbackContext):
        return self.change_step(chat_state, update, lambda s : s.hasPrevious, lambda x: x - 1)

    def change_step(self, chat_state: ChatState, update: Update, get_step, update_index: Callable[[int], int]):
        update.callback_query.answer()
        step = get_step(chat_state.current_step)[0]
        index = update_index(chat_state.step_index)
        chat_state.change_step(step, index)
        chat_state.last_message().edit_text(self.create_step_text(step, index), parse_mode=ParseMode.MARKDOWN_V2)
        chat_state.last_message().edit_reply_markup(self.step_buttons(step))
        return bot_states.VIEWING_STEPS
    
    def create_step_text(self, step, index: int) -> str:
        return escape_text(f"""
*Step {index + 1}*

{step.hasDescription}
""")
    
    def step_buttons(self, step):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="➡️", callback_data=bot_events.NEXT if len(step.hasNext) > 0 else bot_events.BACK)],
            [InlineKeyboardButton(text="⬅️", callback_data=bot_events.PREV if len(step.hasPrevious) > 0 else bot_events.BACK)],
        ])