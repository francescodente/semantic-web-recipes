from bot.state.chat_state import ChatState
from ontology.model import *
from datetime import timedelta

from owlready2 import *

class RecipesOntology:
    def __init__(self, world: World):
        self.world = world

    def get_countries_with_at_least_one_dish(self) -> list[Country]:
        query = """
            PREFIX : <http://www.semanticweb.org/it/unibo/semantic-web/recipes#>

            SELECT DISTINCT ?country ?name (COUNT(?recipe) AS ?n)
            WHERE
            {
                ?recipe :isRecipeFor/:hasOrigin ?country .
                ?country :countryName ?name .
            }
            GROUP BY ?country ?name
            ORDER BY ?name
            """

        return [Country(country.iri, name, count) for country, name, count in self.world.sparql(query)]
    
    def find_dishes(self, chat_state: ChatState) -> list[Dish]:
        where_clause = ""
        params = []

        def add_condition(where_clause, condition):
            return f"{where_clause}\n{condition}"

        if chat_state.selected_country is not None:
            where_clause = add_condition(where_clause, f"?dish :hasOrigin <{chat_state.selected_country.iri}> .")
        
        for i, ingredient in enumerate(chat_state.selected_ingredients):
            param_name = f"?ingr{i}"
            where_clause = add_condition(where_clause, f"""?recipe :containsIngredient/rdfs:label {param_name} FILTER({param_name} = ??) .""")
            params.append(ingredient)

        query = f"""
            PREFIX : <http://www.semanticweb.org/it/unibo/semantic-web/recipes#>

            SELECT ?dish ?dishName ?recipe ?title ?prepTime ?initialStep ?difficulty
            WHERE
            {{
                ?dish rdfs:label ?dishName .
                ?recipe :isRecipeFor ?dish ;
                        :hasTitle ?title ;
                        :hasPreparationTimeInMinutes ?prepTime ;
                        :hasInitialStep ?initialStep ;
                        :hasDifficulty ?difficulty .
                {where_clause}
            }}
        """

        dishes: dict[str, Dish] = {}
        for dish, dish_name, recipe, recipe_title, preparation_time, initial_step, difficulty in self.world.sparql(query, params):
            if dish.iri not in dishes:
                dishes[dish.iri] = Dish(dish.iri, dish_name, [])
            dishes[dish.iri].recipes.append(Recipe(recipe.iri, recipe_title, timedelta(minutes=int(preparation_time)), initial_step, difficulty))
        return list(dishes.values())
    
    def find_recipe_ingredients(self, recipe_iri: str) -> list[Ingredient]:
        query = f"""
            PREFIX : <http://www.semanticweb.org/it/unibo/semantic-web/recipes#>
        
            SELECT ?ingredient ?quantity ?unit
            WHERE
            {{
                <{recipe_iri}> :hasIngredientWithQuantity ?iwq .
                ?iwq :hasIngredient/rdfs:label ?ingredient ;
                     :hasQuantity ?quantity ;
                     :hasMeasurementUnit/rdfs:label ?unit .
            }}
        """

        return [Ingredient(ingredient, quantity, unit) for ingredient, quantity, unit in self.world.sparql(query)]