from bot.telegram_bot import TelegramBot
import os

from ontology.recipes_ontology import RecipesOntology
from owlready2 import *

token = os.getenv("TOKEN")

world = World()
world.get_ontology(os.getenv("ONTOLOGY_IRI")).load()
world.get_ontology(os.getenv("COUNTRIES_IRI")).load()
world.get_ontology(os.getenv("RECIPES_IRI")).load()


onto = world.get_ontology("http://recipes/inferred")

with onto:
    sync_reasoner_hermit(world, infer_property_values=True, keep_tmp_file=True)

bot = TelegramBot(token, RecipesOntology(world))
bot.start()
