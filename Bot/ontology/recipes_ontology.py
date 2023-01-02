from bot.state.chat_state import ChatState
from ontology.model import *

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
            Recipe("Carbonara", 0),
            Recipe("Pesto", 0),
        ]
    
    def find_step(self, id: int) -> Step:
        return Step(f"Step {id}", id + 1 if id < 5 else None, id - 1 if id > 0 else None)