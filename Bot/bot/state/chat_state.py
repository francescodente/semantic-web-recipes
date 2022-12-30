from model.country import Country
from model.recipe import Recipe
from telegram import (Message, ReplyMarkup)
from telegram.ext import CallbackContext

class ChatState:
    def __init__(self, id: int):
        self.id = id
        self.messages_stack: list[Message] = []
        self.reset()

    def set_selected_country(self, country: Country):
        self.country = country
        
    def get_selected_country(self) -> Country | None:
        return self.country
    
    def set_selected_ingredients(self, ingredients: list[str]):
        self.ingredients = ingredients
    
    def get_selected_ingredients(self) -> list[str]:
        return self.ingredients

    def set_recipes(self, recipes: list[Recipe]):
        self.recipes = recipes
    
    def get_recipe(self, recipeName: str) -> Recipe:
        return next(r for r in self.recipes if r.name == recipeName)
    
    def set_selected_recipe(self, recipe: Recipe):
        self.selected_recipe = recipe
    
    def get_selected_recipe(self) -> Recipe | None:
        return self.selected_recipe

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
    
    def reset(self):
        self.country = None
        self.ingredients = []
        self.recipes = []
        self.selected_recipe = None