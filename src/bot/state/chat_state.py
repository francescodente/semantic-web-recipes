from ontology.model import *
from telegram import (Message, ReplyMarkup)
from telegram.ext import CallbackContext

class ChatState:
    def __init__(self, id: int):
        self.id = id
        self.messages_stack: list[Message] = []
        self.countries: list[Country] = []
        self.selected_country: Country | None = None
        self.selected_ingredients: list[Ingredient] = []
        self.search_result: list[Dish] = []
        self.selected_dish: Dish = None
        self.selected_recipe: Recipe = None
        self.step_index = 0
        self.vegan = False

    def toggle_vegan(self):
        self.vegan = not self.vegan
    
    def remember_countries(self, countries: list[Country]):
        self.countries = countries

    def set_selected_country(self, index: int):
        self.selected_country = self.countries[index]
    
    def set_selected_ingredients(self, ingredients: list[str]):
        self.selected_ingredients = ingredients

    def set_search_result(self, dishes: list[Dish]):
        self.search_result = dishes
    
    def get_dish_from_search_result(self, index: int) -> Dish:
        return self.search_result[index]
    
    def set_selected_dish(self, dish: Dish):
        self.selected_dish = dish
    
    def set_selected_recipe(self, recipe: Recipe):
        self.selected_recipe = recipe

    def change_step(self, step, index: int):
        self.step_index = index
        self.current_step = step

    def push_message(self, context: CallbackContext, text: str, parse_mode: str | None = None, reply_markup: ReplyMarkup | None = None):
        message = context.bot.send_message(
            self.id,
            text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
        )
        self.messages_stack.append(message)
    
    def pop_message(self):
        message = self.messages_stack.pop()
        message.delete()

    def last_message(self):
        return self.messages_stack[-1]