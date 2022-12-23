class ChatState:
    def __init__(self, id: int):
        self.id = id
        self.reset()

    def set_selected_country(self, country):
        self.country = country
        
    def get_selected_country(self):
        return self.country
    
    def set_selected_ingredients(self, ingredients):
        self.ingredients = list(ingredients)
    
    def get_selected_ingredients(self):
        return self.ingredients
    
    def reset(self):
        self.country = None
        self.ingredients = []