class ChatState:
    def __init__(self, id: int):
        self.id = id
        self.reset()

    def set_selected_country(self, country):
        self.country = country
        
    def get_selected_country(self):
        return self.country
    
    def add_selected_ingredient(self, ingredient):
        self.ingredients.add(ingredient)

    def remove_ingredient(self, ingredient):
        self.ingredients.remove(ingredient)
    
    def reset(self):
        self.country = None
        self.ingredients = set([])