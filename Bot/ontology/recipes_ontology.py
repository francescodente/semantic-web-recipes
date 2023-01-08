from bot.state.chat_state import ChatState
from ontology.model import *
from datetime import timedelta

from owlready2 import *

class RecipesOntology:
    def __init__(self, ontology_iri):
        self.world = World()
        self.world.get_ontology(ontology_iri).load()
        # sync_reasoner(self.world)

    def __add_condition(self, where_clause: str, filter: str) -> str:
        return f"{where_clause}\n{filter}"

    def get_countries_with_at_least_one_dish(self) -> list[Country]:
        query = """
            PREFIX c: <http://www.bpiresearch.com/BPMO/2004/03/03/cdl/Countries#>
            PREFIX : <http://www.semanticweb.org/it/unibo/semantic-web/recipes#>

            SELECT DISTINCT ?country ?name (COUNT(?recipe) AS ?n)
            WHERE
            {
                ?country a/rdfs:subClassOf* c:Country .
                ?country ^:hasOrigin/:hasRecipe ?recipe .
                ?country c:nameEnglish ?name .
            }
            GROUP BY ?name
            ORDER BY ?name
        """
        return [Country(country.iri, name, count) for country, name, count in self.world.sparql(query)]
    
    def find_dishes(self, chat_state: ChatState) -> list[Dish]:
        where_clause = ""
        args = []

        def add_condition(condition):
            where_clause += f"\n{condition}"

        if chat_state.get_selected_country() is not None:
            add_condition("?recipe :hasOrigin ?? .")
            args.append(chat_state.get_selected_country)
        
        for i, ingredient in enumerate(chat_state.get_selected_ingredients()):
            param_name = f"?ingr{i}"
            add_condition(f"""?recipe :hasIngredient/rdfs:label {param_name} FILTER REGEX({param_name}, ".*({ingredient}).*", "i") .""")

        query = f"""
            PREFIX c: <http://www.bpiresearch.com/BPMO/2004/03/03/cdl/Countries#>
            PREFIX : <http://www.semanticweb.org/it/unibo/semantic-web/recipes#>

            SELECT ?dish ?dishName ?recipe ?title ?prepTime ?initialStep
            WHERE
            {{
                ?dish :hasRecipe ?recipe .
                ?dish rdfs:label ?dishName
                ?recipe :hasTitle ?title .
                ?recipe :hasPreparationTimeInMinutes ?prepTime .
                ?recipe :hasInitialStep ?initialStep .
                {where_clause}
            }}
        """

        dishes: dict[str, Dish] = {}
        for dish, dish_name, recipe, recipe_title, preparation_time, initial_step in self.world.sparql(query):
            if dish.iri not in dishes:
                dishes[dish.iri] = Dish(dish.iri, dish_name, [])
            dishes[dish.iri].recipes.append(Recipe(recipe.iri, recipe_title, timedelta(minutes=preparation_time), initial_step))
    
    def find_recipe_ingredients(self, recipe_iri: str) -> list[Ingredient]:
        return [
            Ingredient("Carrots", 3, "units"),
            Ingredient("Beans", 200, "g"),
        ]

    
    def find_step(self, id: int) -> Step:
        return Step(f"Step {id}", id + 1 if id < 5 else None, id - 1 if id > 0 else None)