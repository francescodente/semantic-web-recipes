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
                ?country a/rdfs:subClassOf* :Country .
                ?country ^:hasOrigin/:hasRecipe ?recipe .
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
                ?dish :hasRecipe ?recipe .
                ?dish rdfs:label ?dishName .
                ?recipe :hasTitle ?title .
                ?recipe :hasPreparationTimeInMinutes ?prepTime .
                ?recipe :hasInitialStep ?initialStep .
                ?recipe :hasDifficulty ?difficulty .
                {where_clause}
            }}
        """

        dishes: dict[str, Dish] = {}
        for dish, dish_name, recipe, recipe_title, preparation_time, initial_step, difficulty in self.world.sparql(query, params):
            if dish.iri not in dishes:
                dishes[dish.iri] = Dish(dish.iri, dish_name, [])
            dishes[dish.iri].recipes.append(Recipe(recipe.iri, recipe_title, timedelta(minutes=int(preparation_time)), initial_step.iri, difficulty))
        return list(dishes.values())
    
    def find_recipe_ingredients(self, recipe_iri: str) -> list[Ingredient]:
        query = f"""
            PREFIX : <http://www.semanticweb.org/it/unibo/semantic-web/recipes#>
        
            SELECT ?name ?quantityValue ?unit
            WHERE
            {{
                <{recipe_iri}> :hasIngredientWithQuantity ?iwq .
                ?iwq :hasIngredient ?ingredient .
                ?iwq :hasQuantity ?quantity .
                ?quantity :hasValue ?quantityValue .
                ?quantity :hasMeasurementUnit ?unit .
                ?ingredient rdfs:label ?name .
                ?unit rdfs:label ?unitName .
            }}
        """

        return [Ingredient(name, quantity, unit.iri) for name, quantity, unit in self.world.sparql(query)]
    
    def find_step(self, step_iri: str) -> Step:
        query = f"""
            PREFIX : <http://www.semanticweb.org/it/unibo/semantic-web/recipes#>

            SELECT ?description ?prev ?next
            WHERE
            {{
                <{step_iri}> :hasDescription ?description .
                OPTIONAL {{ <{step_iri}> :hasPrevious ?prev }} .
                OPTIONAL {{ <{step_iri}> :hasNext ?next }} .
            }}
        """

        def iri_or_none(x):
            return x.iri if x else None
        
        description, prev_step, next_step = next(self.world.sparql(query))
        return Step(description, iri_or_none(next_step), iri_or_none(prev_step))