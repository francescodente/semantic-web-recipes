from bot.telegram_bot import TelegramBot
import os

from ontology.recipes_ontology import RecipesOntology
from owlready2 import *

token = os.getenv("TOKEN")

world = World()
world.get_ontology(os.getenv("ONTOLOGY_IRI")).load()
world.get_ontology(os.getenv("COUNTRIES_IRI")).load()
world.get_ontology(os.getenv("RECIPES_IRI")).load()

sync_reasoner_pellet(world)

# onto = world.get_ontology("http://inferred/recipes")
# with onto:
#     sync_reasoner_hermit(world)

# onto.load()

bot = TelegramBot(token, RecipesOntology(world))
bot.start()
