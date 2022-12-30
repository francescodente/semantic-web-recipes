from bot.state.chat_state import ChatState
from model.recipe import Recipe
from model.country import Country

class RecipesOntology:
    def __init__(self):
        pass

    def get_countries(self) -> list[Country]:
        return [
            Country("Italy"),
            Country("France"),
            Country("Spain"),
            Country("Japan"),
        ]
    
    def find_recipes(self, chat_state: ChatState) -> list[Recipe]:
        return [
            Recipe("Carbonara"),
            Recipe("Pesto"),
        ]